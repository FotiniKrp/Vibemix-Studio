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

    if (!oscReceiver.connect(7000))
    {
        DBG("Error: could not connect to UDP port 7000.");
    }
    else
    {
        DBG("Listening for OSC messages on UDP port 7000.");
        oscReceiver.addListener(this, "/is_fist");
        oscReceiver.addListener(this, "/is_horns");
        oscReceiver.addListener(this, "/is_shaka");
        oscReceiver.addListener(this, "/is_peace");
        oscReceiver.addListener(this, "/pinch_value_right");
        oscReceiver.addListener(this, "/pinch_value_left");
        oscReceiver.addListener(this, "/hand_openness_value_right");
        oscReceiver.addListener(this, "/hand_openness_value_left");
        oscReceiver.addListener(this, "/parallel_palms_distance");
    }
    setSize(1000, 600);

	// initialize reverb parameters


}

MainComponent::~MainComponent()
{
    oscReceiver.removeListener(this);
    oscReceiver.disconnect();

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
    juce::dsp::ProcessSpec spec;
	spec.sampleRate = sampleRate;
    spec.numChannels = 2;
	spec.maximumBlockSize = samplesPerBlockExpected;
    reverb.prepare(spec); 

    juce::dsp::Reverb::Parameters params;
    params.roomSize = 0.7f; // Medium-large room
    params.damping = 0.5f; // Mid frequency absorption
    params.wetLevel = 0.35f; // 35% reverberated sound
    params.dryLevel = 0.65f; // 65% direct mic sound
    params.width = 1.0f;
    params.freezeMode = 0.0f;

    reverb.setParameters(params);
}

void MainComponent::getNextAudioBlock(const juce::AudioSourceChannelInfo& bufferToFill)
{
    // Your audio-processing code goes here!

    // For more details, see the help for AudioProcessor::getNextAudioBlock()

    // Right now we are not producing any data, in which case we need to clear the buffer
    // (to prevent the output of random noise)

    // 1. Get an AudioBlock covering the entire buffer
    juce::dsp::AudioBlock<float> block(*bufferToFill.buffer);

    // 2. Slice the AudioBlock to only process the current active sub-region
    auto subBlock = block.getSubBlock((size_t)bufferToFill.startSample,
        (size_t)bufferToFill.numSamples);

    // 3. Create a processing context using the sub-block
    juce::dsp::ProcessContextReplacing<float> context(subBlock);

    uint32_t current_time = juce::Time::getMillisecondCounter();
	uint32_t last_rpinch_time = last_pinch_right.load(std::memory_order_relaxed);

    // 4. Process the audio live through your reverb instance
	if (current_time - last_rpinch_time < timeoutThresholdMs) {
		float rpinch = pinch_right.load(std::memory_order_relaxed);

        juce::dsp::Reverb::Parameters params;

        // Room Size: Από 0.2f (μικρό δωμάτιο) έως 0.85f (τεράστια αμφιθέατρο)
        params.roomSize = juce::jmap(rpinch, 0.0f, 1.0f, 0.2f, 0.85f);

        // Damping: Όσο πιο ανοιχτά τα δάχτυλα, τόσο λιγότερη απορρόφηση (πιο λαμπερό reverb)
        params.damping = juce::jmap(rpinch, 0.0f, 1.0f, 0.7f, 0.3f);

        // Mix (Wet / Dry)
        // Wet: Από 0.0f (καθόλου Reverb) έως 0.6f (έντονο Reverb)
        params.wetLevel = juce::jmap(rpinch, 0.0f, 1.0f, 0.0f, 0.6f);
        // Dry: Από 1.0f (πλήρης καθαρός ήχος) έως 0.4f (ελαφρώς υποχωρημένος)
        params.dryLevel = 1.0f - (params.wetLevel * 0.5f);

        // 4. Ενημέρωση του Reverb DSP Module
        reverb.setParameters(params);
        reverb.process(context);
	}
}

void MainComponent::releaseResources()
{
    // This will be called when the audio device stops, or when it is being
    // restarted due to a setting change.

    // For more details, see the help for AudioProcessor::releaseResources()
}

//==============================================================================
void MainComponent::paint(juce::Graphics& g)
{
    // (Our component is opaque, so we must completely fill the background with a solid colour)
    g.fillAll(getLookAndFeel().findColour(juce::ResizableWindow::backgroundColourId));

    // You can add your drawing code here!
}

void MainComponent::resized()
{
    audioSetupComp->setBounds(getLocalBounds());
}

void MainComponent::oscMessageReceived(const juce::OSCMessage& message)
{
    auto address = message.getAddressPattern().toString();
	uint32_t current_time = juce::Time::getMillisecondCounter();

    if (address == "/is_fist")
    {
        if (message.size() > 0 && message[0].isInt32())
        {
            int value = message[0].getInt32();
            DBG("Received is_fist value: " << value);
        }
    }
    if (address == "/is_horns")
    {
        if (message.size() > 0 && message[0].isInt32())
        {
            int value = message[0].getInt32();
            DBG("Received is_horns value: " << value);
        }
    }
    if (address == "/is_shaka")
    {
        if (message.size() > 0 && message[0].isInt32())
        {
            int value = message[0].getInt32();
            DBG("Received is_shaka value: " << value);
        }
    }
    if (address == "/is_peace")
    {
        if (message.size() > 0 && message[0].isInt32())
        {
            int value = message[0].getInt32();
            DBG("Received is_peace value: " << value);
        }
    }
    if (address == "/pinch_value_right")
    {
        if (message.size() > 0 && message[0].isFloat32())
        {
            float value = message[0].getFloat32();
			pinch_right.store(value, std::memory_order_relaxed);
            last_pinch_right.store(current_time, std::memory_order_relaxed);
        }
    }
    if (address == "/pinch_value_left")
    {
        if (message.size() > 0 && message[0].isFloat32())
        {
            float value = message[0].getFloat32();
            DBG("Received left-handed pinch value: " << value);
        }
    }
    if (address == "/hand_openness_value_right")
    {
        if (message.size() > 0 && message[0].isFloat32())
        {
            float value = message[0].getFloat32();
            DBG("Received right-handed hand_openness_value: " << value);
        }
    }
    if (address == "/hand_openness_value_left")
    {
        if (message.size() > 0 && message[0].isFloat32())
        {
            float value = message[0].getFloat32();
            DBG("Received left-handed hand_openness_value: " << value);
        }
    }
    if (address == "/parallel_palms_distance")
    {
        if (message.size() > 0 && message[0].isFloat32())
        {
            float value = message[0].getFloat32();
            DBG("Received parallel_palms_distance: " << value);
        }
    }
}