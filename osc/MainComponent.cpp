#include "MainComponent.h"

//==============================================================================
MainComponent::MainComponent() : juce::AudioAppComponent(myDeviceManager),
    oscReceiver()
{
	myDeviceManager.initialise(2, 2, nullptr, true);
    audioSetupComp.reset(new juce::AudioDeviceSelectorComponent(myDeviceManager, 0, 2, 0, 2, true, true, true, true));
	addAndMakeVisible(audioSetupComp.get());
    // Make sure you set the size of the component after
    // you add any child components.
    // Some platforms require permissions to open input channels so request that here
    if (juce::RuntimePermissions::isRequired (juce::RuntimePermissions::recordAudio)
        && ! juce::RuntimePermissions::isGranted (juce::RuntimePermissions::recordAudio))
    {
        juce::RuntimePermissions::request (juce::RuntimePermissions::recordAudio,
                                           [&] (bool granted) { setAudioChannels (granted ? 2 : 0, 2); });
    }
    else
    {
        // Specify the number of input and output channels that we want to open
        setAudioChannels (2, 2);
    }

	if (!oscReceiver.connect(7000))
	{
		DBG("Error: could not connect to UDP port 7000.");
	}
	else
	{
        DBG("Listening for OSC messages on UDP port 7000.");
		oscReceiver.addListener(this, "/number");
	}
    setSize(1000, 600);
  
}

MainComponent::~MainComponent()
{
	oscReceiver.removeListener(this);
	oscReceiver.disconnect();

    // This shuts down the audio device and clears the audio source.
    shutdownAudio();
}

//==============================================================================
void MainComponent::prepareToPlay (int samplesPerBlockExpected, double sampleRate)
{
    // This function will be called when the audio device is started, or when
    // its settings (i.e. sample rate, block size, etc) are changed.

    // You can use this function to initialise any resources you might need,
    // but be careful - it will be called on the audio thread, not the GUI thread.

    // For more details, see the help for AudioProcessor::prepareToPlay()
}

void MainComponent::getNextAudioBlock (const juce::AudioSourceChannelInfo& bufferToFill)
{
    // Your audio-processing code goes here!

    // For more details, see the help for AudioProcessor::getNextAudioBlock()

    // Right now we are not producing any data, in which case we need to clear the buffer
    // (to prevent the output of random noise)
    auto& inputBuffer = *bufferToFill.buffer;

    for (int channel = 0; channel < bufferToFill.buffer->getNumChannels(); ++channel)
    {
        bufferToFill.buffer->copyFrom(channel, bufferToFill.startSample, inputBuffer, channel, bufferToFill.startSample, bufferToFill.numSamples);
    }
}

void MainComponent::releaseResources()
{
    // This will be called when the audio device stops, or when it is being
    // restarted due to a setting change.

    // For more details, see the help for AudioProcessor::releaseResources()
}

//==============================================================================
void MainComponent::paint (juce::Graphics& g)
{
    // (Our component is opaque, so we must completely fill the background with a solid colour)
    g.fillAll (getLookAndFeel().findColour (juce::ResizableWindow::backgroundColourId));

    // You can add your drawing code here!
}

void MainComponent::resized()
{
	audioSetupComp->setBounds(getLocalBounds());
}

void MainComponent::oscMessageReceived(const juce::OSCMessage& message)
{
	if (message.size() > 0)
    {
        if (message[0].isInt32())
        {
			int value = message[0].getInt32();
			DBG("Received int: " << value);
        }
        else if (message[0].isFloat32())
        {
			float value = message[0].getFloat32();
			DBG("Received float: " << value);
        }
    }
}
