#include <iostream>
#include <cstdint>
#include "oscpack/osc/OscPacketListener.h"
#include "oscpack/osc/OscReceivedElements.h"
#include "oscpack/ip/UdpSocket.h"

#define PORT 9000

using namespace std;

class OscListener : public osc::OscPacketListener {
protected:
    virtual void ProcessMessage( const osc::ReceivedMessage& m, const IpEndpointName& remoteEndpoint ) override
    {
        (void) remoteEndpoint; // suppress unused parameter warning

        try{
            if( strcmp( m.AddressPattern(), "/number" ) == 0 ){
                osc::ReceivedMessageArgumentStream args = m.ArgumentStream();
                osc::int32 value;
                args >> value >> osc::EndMessage;
                
                cout << "Received '/number' message with argument: " << value << endl;
            }
        }catch( osc::Exception& e ){
            // any parsing errors such as unexpected argument types, or 
            // missing arguments get thrown as exceptions.
            cout << "error while parsing message: " << m.AddressPattern() << ": " << e.what() << endl;
        }
    }
};

int main()
{
    OscListener listener;
    UdpListeningReceiveSocket socket(IpEndpointName( "127.0.0.1", PORT ), &listener);

    cout << "Listening for OSC messages on port " << PORT << "..." << endl;
    socket.RunUntilSigInt();

    return 0;
}