#ifndef KEY_HPP_INCLUDED
#define KEY_HPP_INCLUDED

#include "context.hpp"
#include "except.hpp"
#include "cert.hpp"
#include "rcobj.hpp"

class Hash;
class Key : public RCObj
{
    HCRYPTKEY hkey;
    RCObj *parent;
public:
    Key(RCObj *pctx, HCRYPTKEY hk) throw(CSPException);

    ~Key() throw(CSPException);

    void encode(BYTE **s, DWORD *slen, Key *cryptkey=NULL) throw(CSPException);

    void store_cert(Cert *c) throw (CSPException);

    void extract_cert(BYTE **s, DWORD *slen) throw (CSPException);

    ALG_ID alg_id() throw (CSPException);

    friend class Crypt;
    friend class Hash;
};

#endif
