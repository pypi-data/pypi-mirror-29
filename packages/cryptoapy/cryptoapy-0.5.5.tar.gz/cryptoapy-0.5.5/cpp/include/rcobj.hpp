#ifndef RCOBJ_HPP_INCLUDED
#define RCOBJ_HPP_INCLUDED

#include "except.hpp"

class RCObj
{
protected:
    signed int refcount;
public:
    RCObj() {
        refcount = 0;
    }

    virtual ~RCObj() throw(CSPException) {};

    int ref();

    int unref();
};

#endif
