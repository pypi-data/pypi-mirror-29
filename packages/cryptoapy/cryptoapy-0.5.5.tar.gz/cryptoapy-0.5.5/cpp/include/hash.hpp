#ifndef HASH_HPP_INCLUDED
#define HASH_HPP_INCLUDED

#include "common.hpp"
#include "rcobj.hpp"
#include "except.hpp"

class Crypt;
class Cert;
class Key;


/**
 * Provides simple hash functions, like data hash calculation, signing and
 * veriying hashes. Used primarily for XML DSIG, for general message signing
 * and verifying see `Msg` class.
 */
class Hash : public RCObj
{
private:
    HCRYPTHASH hhash;
    Crypt *parent;
    Key *pkey;
    void init(Crypt *ctx, Key *key, int length) throw(CSPException);
    HMAC_INFO   HmacInfo;
protected:
    //
public:
    Hash(Crypt *ctx, BYTE *STRING, DWORD LENGTH, Key *key, int length=0) throw(CSPException);
    Hash(Crypt *ctx, BYTE *STRING, DWORD LENGTH, int length=0) throw(CSPException);
    Hash(Crypt *ctx, Key *key, int length=0) throw(CSPException);
    Hash(Crypt *ctx, int length=0) throw(CSPException);

    virtual ~Hash() throw(CSPException);

    void digest(BYTE **s, DWORD *slen) throw(CSPException);
    void update(BYTE *STRING, DWORD LENGTH) throw(CSPException);
    void sign(BYTE **s, DWORD *slen, DWORD dwKeyspec=AT_KEYEXCHANGE) throw(CSPException);
    bool verify(Cert *cert, BYTE *STRING, DWORD LENGTH) throw(CSPException);
    Key *derive_key() throw(CSPException);

    friend class Crypt;
};

#endif
