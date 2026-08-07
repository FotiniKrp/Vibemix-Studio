#pragma once

#include <JuceHeader.h>
#include <juce_dsp/juce_dsp.h>
#include <atomic>

//==============================================================================
/*
    This component lives inside our window, and this is where you should put all
    your controls and content.
*/
class MainComponent  : public juce::AudioAppComponent,
	private juce::OSCReceiver::ListenerWithOSCAddress<juce::OSCReceiver::MessageLoopCallback>
{
public:
    //==============================================================================
    MainComponent();
    ~MainComponent() override;

    //==============================================================================
    void prepareToPlay (int samplesPerBlockExpected, double sampleRate) override;
    void getNextAudioBlock (const juce::AudioSourceChannelInfo& bufferToFill) override;
    void releaseResources() override;

    //==============================================================================
    void paint (juce::Graphics& g) override;
    void resized() override;

private:
    //==============================================================================
    // Your private member variables go here...
    void oscMessageReceived(const juce::OSCMessage& message) override;
	juce::OSCReceiver oscReceiver;
    juce::AudioDeviceManager myDeviceManager;
	std::unique_ptr<juce::AudioDeviceSelectorComponent> audioSetupComp;
    JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR (MainComponent)

    std::atomic<float> pinch_right{ 0.0f };
    std::atomic<uint32_t> last_pinch_right{ 0 };

    const uint32_t timeoutThresholdMs = 200;

	juce::dsp::Reverb reverb; //initialize reverb processor
};
