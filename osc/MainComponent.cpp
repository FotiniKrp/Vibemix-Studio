#include "MainComponent.h"

//==============================================================================
MainComponent::MainComponent()
{
    audioSettings = std::make_unique<juce::AudioDeviceSelectorComponent>(
        deviceManager,
        0, 2,
        0, 2,
        true,
        true,
        true,
        false
    );

    addAndMakeVisible(audioSettings.get());

    // Make sure you set the size of the component after
    // you add any child components.
    setSize(800, 600);

    // Some platforms require permissions to open input channels so request that here
    if (juce::RuntimePermissions::isRequired(juce::RuntimePermissions::recordAudio)
        && !juce::RuntimePermissions::isGranted(juce::RuntimePermissions::recordAudio))
    {
        juce::RuntimePermissions::request(juce::RuntimePermissions::recordAudio,
            [&](bool granted) { setAudioChannels(granted ? 2 : 0, 2); });
    }
    else
    {
        // Specify the number of input and output channels that we want to open
        setAudioChannels(2, 2);
    }

    if (!oscReceiver.connect(9000))
    {
		DBG("Error: Could not connect to UDP port 9000.");
    }
    else
    {
		DBG("Listening for OSC messages on UDP port 9000.");
    }

	oscReceiver.addListener(this, "/test");
}

MainComponent::~MainComponent()
{
    // This shuts down the audio device and clears the audio source.
    shutdownAudio();
}

//==============================================================================
void MainComponent::prepareToPlay(int samplesPerBlockExpected, double sampleRate)
{
    // This function will be called when the audio device is started, or when
    // its settings (i.e. sample rate, block size, etc) are changed.

    // You can use this function to initialise any resources you might need,
    // but be careful - it will be called on the audio thread, not the GUI thread.

    // For more details, see the help for AudioProcessor::prepareToPlay()
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

void MainComponent::getNextAudioBlock(const juce::AudioSourceChannelInfo& bufferToFill)
{
    // Your audio-processing code goes here!

    // For more details, see the help for AudioProcessor::getNextAudioBlock()

    // Right now we are not producing any data, in which case we need to clear the buffer
    // (to prevent the output of random noise)
    // bufferToFill.clearActiveBufferRegion();

    auto* inputBuffer = bufferToFill.buffer;
	auto* device = deviceManager.getCurrentAudioDevice();

	if (device == nullptr)
		return;

	auto inputChannels = device->getActiveInputChannels();
	auto outputChannels = device->getActiveOutputChannels();

    // Αντιγραφή input -> output
    for (int channel = 0; channel < inputBuffer->getNumChannels(); ++channel)
    {
        if (outputChannels[channel])
        {
            if (!inputChannels[channel])
            {
                inputBuffer->clear(channel, bufferToFill.startSample, bufferToFill.numSamples);
            }
        }
    }
}

void MainComponent::releaseResources()
{
    // This will be called when the audio device stops, or when it is being
    // restarted due to a setting change.

    // For more details, see the help for AudioProcessor::releaseResources()
}

//==============================================================================
/*void MainComponent::paint(juce::Graphics& g)
{
    // (Our component is opaque, so we must completely fill the background with a solid colour)
    g.fillAll(getLookAndFeel().findColour(juce::ResizableWindow::backgroundColourId));

    // You can add your drawing code here!
}*/

void MainComponent::paint(juce::Graphics& g)
{
    g.fillAll(juce::Colours::darkgrey);

    g.setColour(juce::Colours::white);
    g.setFont(40.0f);
}

void MainComponent::resized()
{
    // This is called when the MainContentComponent is resized.
    // If you add any child components, this is where you should
    // update their positions.
    audioSettings->setBounds(0, 0, getWidth(), getHeight());
}
