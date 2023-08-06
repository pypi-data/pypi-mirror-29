#ifndef CONTEXT_HPP_INCLUDED
#define CONTEXT_HPP_INCLUDED

#include "rcobj.hpp"
#include "except.hpp"

class Key;
class Hash;
class CryptIter;
class Cert;

class CryptDesc
{
public:
    DWORD type;
    char *name;
    virtual ~CryptDesc()
    {
        delete[] name;
    }
};

class CryptIter
{
    DWORD index;
public:
    CryptIter() throw (CSPException);

    CryptIter *__iter__() {
        return new CryptIter();
    }

    CryptDesc *next() throw (Stop_Iteration, CSPException);
};

class Crypt : public RCObj
{
    HCRYPTPROV hprov;
    char *cont_name;
    char *pr_name;

public:

    Cert *parent;
    Crypt (BYTE *STRING, DWORD LENGTH, DWORD type, DWORD flags, char *name=NULL) throw(CSPException, CSPNotFound);
    Crypt (Cert *pcert) throw(CSPNotFound);
    ~Crypt() throw(CSPException);

    char *name();
    char *uniq_name();
    char *prov_name();
    DWORD prov_type();

    Key *create_key(DWORD flags, DWORD keyspec=AT_KEYEXCHANGE) throw(CSPException);

    Key *get_key(DWORD keyspec=AT_KEYEXCHANGE) throw(CSPException, CSPNotFound);

    Key *import_key(BYTE *STRING, DWORD LENGTH, Key *decrypt=NULL) throw(CSPException);

    void set_password(char *pin, DWORD keyspec=AT_KEYEXCHANGE) throw(CSPException);
    void change_password(char *pin) throw (CSPException);
    void public_key(BYTE **s, DWORD *slen, DWORD keyspec=AT_KEYEXCHANGE) throw(CSPException);
    Key *import_public_key_info(Cert *pcert) throw(CSPException);

    static void remove(BYTE *STRING, DWORD LENGTH, DWORD type, char *name) throw(CSPException, CSPNotFound);

    static CryptIter *enumerate() throw(CSPException);

    friend class Cert;
    friend class Hash;
    friend class CryptMsg;
    friend class Signature;
    friend class CertStore;
    friend class CertRequest;
};


#endif
