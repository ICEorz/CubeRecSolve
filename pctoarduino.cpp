#include <iostream>
#include <Windows.h>
using namespace std;

int main() {
    HANDLE hCom = CreateFile("\\\\.\\COM10", GENERIC_READ | GENERIC_WRITE, 0, NULL, OPEN_EXISTING, 0, NULL);
    if (hCom == INVALID_HANDLE_VALUE) {
        cout << "Port number is invalid" << endl;
        return 0;
    }

    DCB dcb;
    GetCommState(hCom, &dcb);
    dcb.BaudRate = 9600;
    dcb.ByteSize = DATABITS_8;
    dcb.Parity = NOPARITY;
    dcb.StopBits = ONESTOPBIT;
    BOOL br = SetCommState(hCom, &dcb);
    COMMTIMEOUTS cto = {MAXWORD, MAXWORD, MAXWORD, MAXWORD, MAXWORD};
    br = SetCommTimeouts(hCom, &cto);

    for (;;) {
        int nInput = 0;
        cin >> nInput;
        if (nInput > 255 || nInput < 0) {
            break;
        }
        BYTE byVal = (BYTE)nInput;
        DWORD dwTransmitted;
        WriteFile(hCom, &byVal, sizeof(byVal), &dwTransmitted, NULL);
    }
    CloseHandle(hCom);
    return 0;
}
