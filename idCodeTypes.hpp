#ifndef _ID_CODE_TYPE_
#define _ID_CODE_TYPE_
#include <string>

const std::string EM_MARINE = "0123456789";
const std::string HID_PROX = "123-45678";
const std::string MIFARE = "AB CD 12 34";

std::string getId (){
    return EM_MARINE;
}

#endif