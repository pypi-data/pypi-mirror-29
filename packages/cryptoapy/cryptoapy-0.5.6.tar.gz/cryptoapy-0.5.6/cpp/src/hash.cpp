#include "hash.hpp"
#include "context.hpp"
#include "cert.hpp"
#include "key.hpp"

ALG_ID hashCAlg(int length) {
    if (2001 == length) {
        return CALG_GR3411;
    }
    if (512 == length) {
        return CALG_GR3411_2012_512;
    }
    return CALG_GR3411_2012_256;
}

void Hash::init(Crypt *ctx, Key *key, int length) throw(CSPException)
{
    HCRYPTKEY  hKey = key? key->hkey: 0;
    parent = 0;
    pkey = 0;
    if(!CryptCreateHash(
        ctx->hprov,
        hashCAlg(length), 
        hKey, 
        0, 
        &hhash)) 
    {
        throw CSPException("Hash::init() failed");
    }
    if (key) {
        // XXX: КриптоПро на это плюется, хотя и надо бы установить параметры

        //ZeroMemory(&HmacInfo, sizeof(HmacInfo));
        //HmacInfo.HashAlgid = CALG_GR3411;
        //if (!CryptSetHashParam(
            //hhash,                // handle of the HMAC hash object
            //HP_HMAC_INFO,             // setting an HMAC_INFO object
            //(BYTE*)&HmacInfo,         // the HMAC_INFO object
            //0))                       // reserved
        //{
            //throw CSPException("Hash::init() failed to set HMAC info");
        //}
        pkey = key;
        pkey->ref();
    }
    parent = ctx;
    parent->ref();
}

/**
 * \~english
 * Create hash from initial data
 *
 * * ctx -- `csp.Crypt`, used for hashing, signing and verifying
 * * STRING, LENGTH -- initial binary data.
 * * key -- `csp.Key`, if present, hash is created as HMAC
 * 
 * \~russian
 * Создание хэша из начальных данных
 *
 * * ctx -- Экземпляр `csp.Crypt` для хэширования, подписывания и проверки * подписи
 * * STRING, LENGTH -- начальные данные.
 * * key -- `csp.Key`, если задан, хэш будет создан как HMAC
 *
 */
Hash::Hash(Crypt *ctx, BYTE *STRING, DWORD LENGTH, Key *key, int length) throw(CSPException)
{
    init(ctx, key, length);
    this->update(STRING, LENGTH);
}

Hash::Hash(Crypt *ctx, BYTE *STRING, DWORD LENGTH, int length) throw(CSPException)
{
    init(ctx, 0, length);
    this->update(STRING, LENGTH);
}

Hash::Hash(Crypt *ctx, Key *key, int length) throw(CSPException)
{
    init(ctx, key, length);
}

Hash::Hash(Crypt *ctx, int length) throw(CSPException)
{
    init(ctx, 0, length);
}


Hash::~Hash() throw(CSPException)
{
    if (hhash && !CryptDestroyHash(hhash)) {
        throw CSPException("~Hash: Couldn't release handle");
    }
    if (parent) {
        parent->unref();
    }
    if (pkey) {
        pkey->unref();
    }
}

void Hash::digest(BYTE **s, DWORD *slen) throw(CSPException) 
{
    DWORD n = sizeof(DWORD);
    if (!CryptGetHashParam(hhash, HP_HASHSIZE, (PBYTE)slen, &n, 0)) {
        throw CSPException("Hash.digest(): Couldn't determine hash size");
    }
    *s = (BYTE*)malloc(*slen);
    if (!CryptGetHashParam(hhash, HP_HASHVAL, *s, slen, 0)) {
        DWORD err = GetLastError();
        free((void *)*s);
        throw CSPException("Hash.digest(): Couldn't get hash value", err);
    }
}

void Hash::update(BYTE *STRING, DWORD LENGTH) throw(CSPException)
{
    if(!CryptHashData(
        hhash, 
        STRING, 
        LENGTH, 
        0)) 
    {
        throw CSPException("Hash::update() failed");
    }
}

void Hash::sign(BYTE **s, DWORD *slen, DWORD dwKeyspec) throw(CSPException) 
{
    if(!CryptSignHash(
        hhash, 
        dwKeyspec, 
        NULL, 
        0, 
        NULL, 
        slen)) 
    {
        throw CSPException("Hash.sign(): Couldn't determine signature size");
    }

    *s = (BYTE*)malloc(*slen);

    if (!CryptSignHash(
        hhash, 
        dwKeyspec, 
        NULL, 
        0, 
        *s, 
        slen)) 
    {
        DWORD err = GetLastError();
        free((void *)*s);
        throw CSPException("Hash.sign(): Couldn't get signature value", err);
    }
}

/**
 * \~russian
 * Проверка подписи под данными, полученной путем вызова `Hash::sign`
 *
 * * `cert` -- сертификат с открытым ключом для проверки
 * * `STRING`, `LENGTH` -- подпись в виде бинарной строки
 *
 * На момент вызова данные должны быть загружены в хэш путем начальной
 * инициализации или вызовом `Hash::update()`.
 * \~english
 * Test Test Test
 *
 */
bool Hash::verify(Cert *cert, BYTE *STRING, DWORD LENGTH) throw (CSPException)
{
    HCRYPTKEY hPubKey = 0;
    // Get the public key from the certificate
    if (!CryptImportPublicKeyInfo(
        parent->hprov, 
        MY_ENC_TYPE,
        &cert->pcert->pCertInfo->SubjectPublicKeyInfo,
        &hPubKey))
    {
        throw CSPException("Hash.verify(): Couldn't get certificate public key handle");
    }

    if (!CryptVerifySignature(
            hhash, 
            STRING, 
            LENGTH, 
            hPubKey,
            NULL, 
            0
        ))
    {
        DWORD err = GetLastError();
        if (err == NTE_BAD_SIGNATURE) {
            return false;
        }
        throw CSPException("Hash.verify(): error verifying hash", err);
    }
    return true;
}

Key *Hash::derive_key() throw(CSPException) 
{
    HCRYPTKEY hkey;

    if (!CryptDeriveKey(
        parent->hprov,                    // handle of the CSP
        CALG_G28147,                 // algorithm ID
        hhash,                    // handle to the hash object
        CRYPT_EXPORTABLE,                        // flags
        &hkey))                   // address of the key handle
    {
        throw CSPException("Hash.derive_key(): error deriving key");
    }
    return new Key(this, hkey);
}
