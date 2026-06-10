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
            if( strcmp( m.AddressPattern(), "/is_fist" ) == 0 ){
                osc::ReceivedMessageArgumentStream args = m.ArgumentStream();
                osc::int32 is_fist;
                args >> is_fist >> osc::EndMessage;
                
                if (is_fist)
                    cout << "FIST DETECTED" << endl;
            }
            else if( strcmp( m.AddressPattern(), "/pinch_value" ) == 0 ){
                osc::ReceivedMessageArgumentStream args = m.ArgumentStream();
                float pinch_value;
                args >> pinch_value >> osc::EndMessage;
                
                cout << "Pinching with value: " << pinch_value << endl;
            }
            else if( strcmp( m.AddressPattern(), "/hand_openness_value" ) == 0 ){
                osc::ReceivedMessageArgumentStream args = m.ArgumentStream();
                float hand_openness_value;
                args >> hand_openness_value >> osc::EndMessage;
                
                cout << "Hand openness value: " << hand_openness_value << endl;
            }
            else if( strcmp( m.AddressPattern(), "/is_horns" ) == 0 ){
                osc::ReceivedMessageArgumentStream args = m.ArgumentStream();
                osc::int32 is_horns;
                args >> is_horns >> osc::EndMessage;
                
                if (is_horns)
                    cout << "HORNS GESTURE" << endl;
            }
            else if( strcmp( m.AddressPattern(), "/is_shaka" ) == 0 ){
                osc::ReceivedMessageArgumentStream args = m.ArgumentStream();
                osc::int32 is_shaka;
                args >> is_shaka >> osc::EndMessage;
                
                if (is_shaka)
                    cout << "TELEPHONE!" << endl;
            }
            else if ( strcmp( m.AddressPattern(), "/parallel_palms_distance" ) == 0 ){
                osc::ReceivedMessageArgumentStream args = m.ArgumentStream();
                float parallel_palms_distance;
                args >> parallel_palms_distance >> osc::EndMessage;
                
                cout << "Distance between parallel palms: " << parallel_palms_distance << endl;
            }
            else if ( strcmp( m.AddressPattern(), "/is_peace" ) == 0 ){
                osc::ReceivedMessageArgumentStream args = m.ArgumentStream();
                osc::int32 is_peace;
                args >> is_peace >> osc::EndMessage;
                
                if (is_peace)
                    cout << "PEACE SIGN!" << endl;
            }
            else {
                cout << "Unknown message received: " << m.AddressPattern() << endl;
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
