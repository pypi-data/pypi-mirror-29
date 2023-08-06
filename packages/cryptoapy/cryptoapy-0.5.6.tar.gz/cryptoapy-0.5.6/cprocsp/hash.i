/* vim: ft=swig
*/

%feature("ref") Hash "$this->ref();"
%feature("unref") Hash "$this->unref();"
%newobject Hash::derive_key;
%include "hash.hpp"
