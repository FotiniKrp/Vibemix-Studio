import React from 'react';
import { Mic, Video, Layers, Sliders, Waves, Play, Square, Circle, Import, Settings, Activity, Hand, Sparkles, Send, MessageSquare, Bot } from 'lucide-react';
import { motion, AnimatePresence } from 'motion/react';
import { Button } from '@/components/ui/button';
import { Slider } from '@/components/ui/slider';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Card } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Toaster } from '@/components/ui/sonner';
import { toast } from 'sonner';

// --- Sub-components ---

const EffectModule = ({ name, icon: Icon, activeColor }: { name: string, icon: any, activeColor: string }) => (
    <motion.div
    whileHover={{ scale: 1.02 }}
    className="p-4 rounded-2xl bg-white/5 border border-white/10 group cursor-pointer relative overflow-hidden"
  >
    <div className="flex items-center justify-between mb-4">
      <div className="flex items-center gap-3">
        <div className={`p-2 rounded-lg bg-black/20 border border-white/5 group-hover:border-${activeColor}-500/50 transition-colors`}>
          <Icon className={`w-5 h-5 group-hover:text-${activeColor}-400 transition-colors`} />
        </div>
        <span className="font-medium text-sm tracking-tight text-white">{name}</span>
      </div>
      <Badge variant="outline" className="text-[10px] uppercase tracking-widest opacity-50 border-white/20 text-white">Active</Badge>
    </div>
    
    <div className="space-y-4">
      <div className="space-y-2">
        <div className="flex justify-between text-[10px] text-muted-foreground uppercase tracking-wider">
          <span>Intensity</span>
          <span>85%</span>
        </div>
        <Slider defaultValue={[85]} max={100} step={1} className="[&_[role=slider]]:bg-primary" />
      </div>

       {/* Gesture Touch Area Mock */}
      <div className="h-24 w-full bg-background/50 rounded-lg border border-dashed border-border/50 flex flex-col items-center justify-center gap-2 group-hover:bg-background/80 transition-all">
        <Hand className="w-5 h-5 text-muted-foreground group-hover:text-primary transition-colors animate-pulse" />
        <span className="text-[10px] text-muted-foreground font-mono">GESTURE AREA</span>
      </div>
    </div>

    {/* Subtle glow highlight */}
    <div className={`absolute -bottom-2 -right-2 w-12 h-12 bg-${activeColor}-500/10 blur-xl rounded-full opacity-0 group-hover:opacity-100 transition-opacity`} />
  </motion.div>
);

const TrackLane = ({ name, color, active = false }: { name: string, color: string, active?: boolean }) => (
  <div className={`group flex items-center gap-4 p-3 rounded-xl border border-white/5 ${active ? 'bg-white/10' : 'hover:bg-white/5'} transition-colors`}>
    <div className="w-48 flex flex-col gap-1">
      <div className="flex items-center justify-between">
        <span className="text-sm font-medium text-white">{name}</span>
        <div className="flex gap-2">
          <Button variant="ghost" size="icon" className="h-6 w-6 opacity-0 group-hover:opacity-100 text-white/50"><Settings className="w-3 h-3" /></Button>
        </div>
      </div>
      <div className="flex items-center gap-2">
        <div className={`w-2 h-2 rounded-full bg-${color}-500 ${active ? 'animate-pulse shadow-[0_0_10px_rgba(var(--color-primary),0.5)]' : 'opacity-50'}`} />
        <div className="h-1 flex-1 bg-white/10 rounded-full overflow-hidden">
          <motion.div 
            initial={{ width: '30%' }}
            animate={{ width: active ? '70%' : '30%' }}
            transition={{ repeat: Infinity, duration: 2, repeatType: 'reverse' }}
            className={`h-full bg-${color}-500/50`} 
          />
        </div>
      </div>
    </div>
    
    <div className="flex-1 h-12 bg-background/40 rounded-md border border-border/20 relative overflow-hidden flex items-center">
        {/* Mock Waveform */}
        <div className="absolute inset-0 flex items-center justify-around gap-1 px-4 opacity-30">
            {Array.from({ length: 40 }).map((_, i) => (
                <motion.div
                    key={i}
                    animate={{ height: [10, 24, 15, 30][i % 4] }}
                    transition={{ repeat: Infinity, duration: 0.5 + i * 0.05, repeatType: 'mirror' }}
                    className={`w-1.5 bg-${color}-500 rounded-full`}
                />
            ))}
        </div>
        {active && (
            <motion.div 
                animate={{ x: [0, 400] }}
                transition={{ duration: 10, repeat: Infinity, ease: "linear" }}
                className="absolute top-0 bottom-0 w-px bg-white/50 shadow-[0_0_8px_rgba(255,255,255,0.5)] z-10"
            />
        )}
    </div>
  </div>
);

export default function AudioLayout() {
  const [isRecording, setIsRecording] = React.useState(false);
  const [isAssistantOpen, setIsAssistantOpen] = React.useState(false);
  const [chatMessages, setChatMessages] = React.useState([
    {
      id: '1',
      sender: 'assistant' as const,
      text: "Yo! I'm your AI Co-Producer. I'm tracking your vocal mix and gesture inputs in real-time. Try raising your hand higher to expand the Cathedral room space!",
      timestamp: '15:03'
    },
    {
      id: '2',
      sender: 'user' as const,
      text: "Can you help me make my vocals sound a bit warmer?",
      timestamp: '15:04'
    },
    {
      id: '3',
      sender: 'assistant' as const,
      text: "Got you! I've dialed up the low-end warmth in Spectral Delay and optimized the compressor threshold. Take a listen and try tilting your palm left to sweep the frequency low-pass.",
      timestamp: '15:04'
    }
  ]);
  const [inputVal, setInputVal] = React.useState('');
  const [isTyping, setIsTyping] = React.useState(false);

  const handleSendMessage = (text: string) => {
    if (!text.trim()) return;
    const userMsg = {
      id: Date.now().toString(),
      sender: 'user' as const,
      text,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    };
    setChatMessages(prev => [...prev, userMsg]);
    setInputVal('');
    setIsTyping(true);

    setTimeout(() => {
      let replyText = "Awesome adjust. I've updated the gesture parameters dynamically. Sweep your palm to hear the difference!";
      const lower = text.toLowerCase();
      if (lower.includes('warm') || lower.includes('equal') || lower.includes('eq')) {
        replyText = "Optimizing EQ curves right now! Boosting the 200Hz region for vocal presence and dialing in some light tube saturation.";
      } else if (lower.includes('gesture') || lower.includes('hand') || lower.includes('map')) {
        replyText = "Gesture mapping is synchronized with the camera tracker. Vertical hand movements are mapped to Aura Reverb mix level, and horizontal movements govern Spectral Delay frequency!";
      } else if (lower.includes('reverb') || lower.includes('echo') || lower.includes('space')) {
        replyText = "Expanding the virtual acoustic space! I've engaged the cathedral preset on the Aura Reverb module.";
      } else if (lower.includes('record') || lower.includes('save') || lower.includes('start')) {
        replyText = "Ready to record! Hit that big RED REC button at the bottom whenever you're ready to lay down the tracks and gesture automations.";
      }
      
      const assistantMsg = {
        id: (Date.now() + 1).toString(),
        sender: 'assistant' as const,
        text: replyText,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      };
      
      setChatMessages(prev => [...prev, assistantMsg]);
      setIsTyping(false);
      toast("Producer Tip Added", { description: "AI adjusted your master output mix." });
    }, 1200);
  };

  const toggleRecording = () => {
    setIsRecording(!isRecording);
    if (!isRecording) {
      toast("Recording started", { description: "Capturing gestures and audio input..." });
    } else {
      toast.success("Recording saved", { description: "Clip added to your workspace." });
    }
  };

  return (
    <div className="h-screen w-full bg-[#0A0A12] [background-image:var(--background-image-frosted)] text-white flex flex-col overflow-hidden font-sans selection:bg-indigo-500/30">
      {/* --- Header --- */}
      <header className="h-16 border-b border-white/5 flex items-center justify-between px-8 bg-white/[0.02] backdrop-blur-md z-50">
        <div className="flex items-center gap-4">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center shadow-lg shadow-indigo-500/20">
            <Waves className="text-white w-6 h-6" />
          </div>
          <div>
            <h1 className="text-lg font-bold tracking-tight leading-none group flex items-center gap-2">
              VIBEMIX <span className="text-indigo-400">STUDIO</span>
              <Badge variant="outline" className="text-[10px] border-indigo-500/20 text-indigo-400">v1.2.0</Badge>
            </h1>
            <p className="text-[10px] text-white/40 uppercase tracking-[0.2em] mt-1 font-bold">Spatial Audio Engine</p>
          </div>
        </div>

        <div className="flex items-center gap-6">
          <div className="flex items-center gap-2 px-4 py-1.5 rounded-full bg-white/5 border border-white/10">
            <div className="flex gap-1 items-end h-3">
              <div className="w-1 bg-green-500 h-2 animate-bounce" style={{ animationDelay: '0.1s' }} />
              <div className="w-1 bg-green-500 h-3 animate-bounce" style={{ animationDelay: '0.3s' }} />
              <div className="w-1 bg-green-500 h-1 animate-bounce" style={{ animationDelay: '0.2s' }} />
            </div>
            <span className="text-xs font-mono text-green-400 tracking-tighter">00:14:02 : 12</span>
          </div>

          <div className="flex gap-2">
            <div className="w-8 h-8 rounded-full bg-gradient-to-tr from-indigo-500 to-purple-500 p-[1px]">
                <div className="w-full h-full rounded-full bg-[#0A0A12] flex items-center justify-center text-[10px] font-bold">JD</div>
            </div>
            <Button variant="ghost" size="icon" className="hover:bg-white/10 text-white/60">
              <Settings className="w-5 h-5" />
            </Button>
          </div>
        </div>
      </header>

      <main className="flex-1 flex overflow-hidden relative">
        {/* Decorative Light Effects */}
        <div className="absolute top-[-10%] right-[-10%] w-[40%] h-[40%] bg-indigo-500/10 blur-[120px] pointer-events-none rounded-full"></div>
        <div className="absolute bottom-[-10%] left-[-10%] w-[30%] h-[30%] bg-pink-500/10 blur-[100px] pointer-events-none rounded-full"></div>

        {/* --- Left Sidebar: Effect Controls --- */}
        <aside className="w-80 border-r border-white/10 flex flex-col bg-white/5 backdrop-blur-2xl z-20">
          <div className="p-6 border-b border-white/5 flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Sliders className="w-4 h-4 text-indigo-400" />
              <h2 className="text-[10px] font-bold uppercase tracking-[0.2em] text-indigo-300">Modules</h2>
            </div>
            <Button 
              variant="outline" 
              size="sm" 
              onClick={() => setIsAssistantOpen(!isAssistantOpen)} 
              className={`h-7 px-2.5 rounded-full border text-[10px] font-bold uppercase tracking-widest transition-all flex items-center gap-1.5 cursor-pointer ${isAssistantOpen ? 'bg-indigo-500/15 border-indigo-400/50 text-indigo-300' : 'bg-white/5 border-white/10 hover:bg-white/10 text-white/80'}`}
            >
              <Sparkles className={`w-3 h-3 ${isAssistantOpen ? 'text-indigo-400 animate-pulse' : 'text-purple-400'}`} />
              {isAssistantOpen ? 'Active' : 'Start'}
            </Button>
          </div>
          
          <ScrollArea className="flex-1">
            <div className="p-6 space-y-4">
              <EffectModule name="Spectral Delay" icon={Waves} activeColor="indigo" />
              <EffectModule name="Vocal Morph" icon={Sparkles} activeColor="purple" />
              <EffectModule name="Aura Reverb" icon={Layers} activeColor="emerald" />
              <EffectModule name="Dynamic Comp" icon={Activity} activeColor="orange" />
              <EffectModule name="Phaser Flux" icon={Waves} activeColor="cyan" />
              <EffectModule name="Granular Synth" icon={Sparkles} activeColor="pink" />
              <EffectModule name="Bit Crusher" icon={Activity} activeColor="amber" />
            </div>
          </ScrollArea>
          
          <div className="p-6 border-t border-white/10 space-y-4">
            <div className="p-4 rounded-xl bg-indigo-500/10 border border-indigo-500/20">
              <div className="flex items-center gap-2 mb-2">
                <Hand className="w-4 h-4 text-indigo-400" />
                <span className="text-[10px] font-bold uppercase tracking-wider text-indigo-300">Gesture Helper</span>
              </div>
              <p className="text-[11px] text-white/60 leading-relaxed font-medium">
                Move your hand up/down to adjust mix intensity. Side-to-side for frequency sweep.
              </p>
            </div>
          </div>
        </aside>

        {/* --- AI Producer Assistant Drawer/Panel Content --- */}
        <AnimatePresence>
          {isAssistantOpen && (
            <motion.div
              initial={{ width: 0, opacity: 0 }}
              animate={{ width: 340, opacity: 1 }}
              exit={{ width: 0, opacity: 0 }}
              transition={{ type: "spring", stiffness: 350, damping: 30 }}
              className="border-r border-white/10 h-full bg-white/[0.03] backdrop-blur-3xl z-20 flex flex-col overflow-hidden"
            >
              {/* Header */}
              <div className="p-5 border-b border-white/5 flex flex-col gap-1.5 bg-white/[0.01]">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <div className="p-1.5 rounded-lg bg-indigo-500/10 border border-indigo-500/30">
                        <Bot className="w-4 h-4 text-indigo-400" />
                    </div>
                    <span className="text-xs font-bold uppercase tracking-[0.15em] text-white">Co-Producer AI</span>
                  </div>
                  <Badge variant="outline" className="text-[9px] text-green-400 border-green-500/20 bg-green-500/10 px-2 py-0.5 animate-pulse">
                    Online
                  </Badge>
                </div>
                <p className="text-[10px] text-white/40 font-medium font-sans">Providing dynamic audio engineering tips</p>
              </div>

              {/* Message Thread */}
              <ScrollArea className="flex-1 p-4">
                <div className="space-y-4">
                  {chatMessages.map((msg) => (
                    <div
                      key={msg.id}
                      className={`flex flex-col ${msg.sender === 'user' ? 'items-end' : 'items-start'}`}
                    >
                      <div className="flex items-center gap-1.5 mb-1.5 px-1">
                        {msg.sender === 'assistant' ? (
                          <>
                            <Bot className="w-3 h-3 text-indigo-400" />
                            <span className="text-[9px] text-white/40 uppercase tracking-widest font-bold">Producer Assistant</span>
                          </>
                        ) : (
                          <>
                            <span className="text-[9px] text-indigo-400 uppercase tracking-widest font-bold">You (JD)</span>
                          </>
                        )}
                        <span className="text-[8px] text-white/20 font-mono">{msg.timestamp}</span>
                      </div>
                      <div
                        className={`p-3.5 rounded-2xl text-[11px] max-w-[88%] leading-relaxed ${
                          msg.sender === 'user'
                            ? 'bg-indigo-600/95 text-white shadow-[0_4px_12px_rgba(99,102,241,0.25)] border border-indigo-500/30 rounded-tr-none'
                            : 'bg-white/5 border border-white/5 text-white/90 rounded-tl-none font-medium'
                        }`}
                      >
                        {msg.text}
                      </div>
                    </div>
                  ))}

                  {isTyping && (
                    <div className="flex flex-col items-start">
                      <div className="flex items-center gap-1.5 mb-1.5 px-1">
                        <Bot className="w-3 h-3 text-indigo-400" />
                        <span className="text-[9px] text-white/40 uppercase tracking-widest font-bold">Producer AI</span>
                      </div>
                      <div className="p-3.5 rounded-2xl rounded-tl-none bg-white/5 border border-white/5 flex items-center gap-1">
                        <span className="w-1.5 h-1.5 bg-indigo-400 rounded-full animate-bounce" style={{ animationDelay: '0s' }} />
                        <span className="w-1.5 h-1.5 bg-indigo-400 rounded-full animate-bounce" style={{ animationDelay: '0.15s' }} />
                        <span className="w-1.5 h-1.5 bg-indigo-400 rounded-full animate-bounce" style={{ animationDelay: '0.3s' }} />
                      </div>
                    </div>
                  )}
                </div>
              </ScrollArea>

              {/* Suggested Preset Prompt Chips */}
              <div className="px-4 py-3 flex flex-wrap gap-1.5 border-t border-white/5 bg-black/15">
                {[
                  "Optimize warmth",
                  "Explain dynamic sweep",
                  "Cathedral room setup"
                ].map((chip, idx) => (
                  <button
                    key={idx}
                    type="button"
                    onClick={() => handleSendMessage(chip)}
                    className="text-[10px] text-indigo-300 hover:text-white bg-indigo-500/5 hover:bg-indigo-500/20 border border-indigo-500/20 rounded-full px-2.5 py-1 text-left transition-all active:scale-95 duration-100 cursor-pointer"
                  >
                    {chip}
                  </button>
                ))}
              </div>

              {/* Chat Form Submit */}
              <form
                onSubmit={(e) => {
                  e.preventDefault();
                  handleSendMessage(inputVal);
                }}
                className="p-3.5 bg-black/20 border-t border-white/5 flex items-center gap-2"
              >
                <input
                  type="text"
                  value={inputVal}
                  onChange={(e) => setInputVal(e.target.value)}
                  placeholder="Type a message to the producer..."
                  className="flex-1 bg-white/5 border border-white/10 rounded-xl px-3 py-2 text-xs text-white placeholder-white/30 focus:outline-none focus:border-indigo-500/50 focus:ring-1 focus:ring-indigo-500/50 transition-all font-medium"
                />
                <Button
                  type="submit"
                  disabled={!inputVal.trim()}
                  className="h-8 w-8 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white border-0 flex items-center justify-center p-0 cursor-pointer disabled:opacity-40 disabled:cursor-not-allowed"
                >
                  <Send className="w-3.5 h-3.5" />
                </Button>
              </form>
            </motion.div>
          )}
        </AnimatePresence>

        {/* --- Center Content Area --- */}
        <div className="flex-1 flex flex-col relative overflow-hidden">
          
          {/* Top Row: Visualizers / Video */}
          <div className="flex-1 p-8 flex gap-8 items-start justify-end relative">
            
            {/* Spectral Waveform Placeholder in main area */}
            <div className="absolute inset-0 flex flex-col items-center justify-center pointer-events-none">
                 <div className="flex items-end gap-1.5 h-32 opacity-20">
                    {Array.from({ length: 48 }).map((_, i) => (
                        <motion.div
                            key={i}
                            animate={{ height: [10, 40, 20, 60, 30][i % 5] }}
                            transition={{ repeat: Infinity, duration: 1 + i * 0.1, repeatType: 'mirror' }}
                            className={`w-1 rounded-full ${i % 2 === 0 ? 'bg-indigo-400' : 'bg-purple-400'}`}
                        />
                    ))}
                </div>
                <p className="mt-6 text-white/20 text-[10px] font-bold uppercase tracking-[0.4em]">Real-time Spectral Engine</p>
            </div>

            {/* Live Feedback Video (Floating Top Right) */}
            <motion.div 
               drag
               dragConstraints={{ left: -400, right: 0, top: 0, bottom: 400 }}
               className="w-80 h-48 rounded-2xl bg-black/60 backdrop-blur-xl border border-white/20 shadow-2xl relative overflow-hidden group cursor-grab active:cursor-grabbing z-30"
            >
                  {/* Live Hand-Tracking Video Stream */}
                <div className="absolute inset-0 bg-[#1A1A2E]/50 flex items-center justify-center overflow-hidden">
                  <img 
                    src="http://localhost:8000/video" 
                    alt="Hand Tracking Live Stream" 
                    className="w-full h-full object-cover"
                    onError={(e) => {
                      console.error("Failed to connect to backend stream on port 8000.");
                    }}
                  />
                </div>
                <div className="absolute top-3 left-3 flex items-center gap-2">
                    <div className="w-2 h-2 rounded-full bg-emerald-500" />
                    <span className="text-[10px] font-bold text-white bg-black/50 px-2 py-0.5 rounded-full backdrop-blur-sm border border-white/10">LIVE FEED</span>
                </div>

                <div className="absolute bottom-3 left-3 right-3 flex justify-between items-end z-10 opacity-0 group-hover:opacity-100 transition-opacity">
                    <div className="bg-black/50 backdrop-blur-md px-2 py-1 rounded text-[9px] border border-white/10 italic text-white/80">Gesture: Tracking active...</div>
                    <Button variant="ghost" size="icon" className="h-6 w-6 text-white"><Settings className="w-3 h-3" /></Button>
                </div>
            </motion.div>
          </div>

          {/* --- Bottom Mixing Station --- */}
          <div className="h-[400px] border-t border-white/10 bg-white/[0.03] backdrop-blur-xl flex flex-col z-20">
            <div className="px-8 py-4 border-b border-white/5 flex items-center justify-between">
              <div className="flex items-center gap-8">
                <div className="flex items-center gap-2">
                  <Layers className="w-4 h-4 text-emerald-400" />
                  <h3 className="text-[10px] font-bold uppercase tracking-[0.2em] text-white/80">Mixing Station</h3>
                </div>
                <div className="flex gap-4">
                  <Button variant="outline" size="sm" className="h-9 px-4 rounded-full text-[10px] uppercase font-bold tracking-widest border-white/10 bg-white/5 hover:bg-white/10 text-white">
                    <Import className="w-4 h-4 mr-2 text-indigo-400" /> Import Audio
                  </Button>
                </div>
              </div>
              
              <div className="flex items-center gap-4">
                <div className="flex gap-2">
                    <Button variant="ghost" size="icon" className="h-10 w-10 border border-white/10 bg-white/5 hover:bg-white/10">
                        <Play className="w-4 h-4 fill-white text-white" />
                    </Button>
                </div>
                
                <div className="h-8 w-[1px] bg-white/10" />

                <Button 
                    onClick={toggleRecording}
                    className={`h-12 w-28 rounded-full shadow-2xl transition-all border-none ${isRecording ? 'bg-red-500 hover:bg-red-600 shadow-[0_0_20px_rgba(239,68,68,0.4)] animate-pulse' : 'bg-indigo-600 hover:bg-indigo-700 shadow-[0_0_20px_rgba(79,70,229,0.4)]'}`}
                >
                  {isRecording ? <Square className="w-4 h-4 mr-2" /> : <div className="w-3 h-3 rounded-full bg-white mr-2" />}
                  <span className="text-xs font-bold uppercase tracking-widest text-white">{isRecording ? 'STOP' : 'REC'}</span>
                </Button>
              </div>
            </div>

            <ScrollArea className="flex-1">
              <div className="p-6 space-y-3">
                <TrackLane name="VOICE MAIN" color="indigo" active={isRecording} />
                <TrackLane name="ATMOS LOOP" color="emerald" />
                <TrackLane name="SFX LAYER" color="purple" />
                <TrackLane name="SYNTH BASS" color="amber" />
                <TrackLane name="DRUM TRACK" color="pink" />
                <TrackLane name="GUITAR RIG" color="cyan" />
              </div>
            </ScrollArea>

            {/* Mixer Master Controls */}
            <div className="h-16 border-t border-white/5 px-8 flex items-center justify-between text-white/40">
               <div className="flex items-center gap-4">
                    <span className="text-[10px] uppercase font-bold tracking-widest">Master Out</span>
                    <div className="w-48 h-1.5 bg-white/5 rounded-full overflow-hidden flex border border-white/5">
                        <div className="h-full bg-gradient-to-r from-indigo-500 to-purple-500 w-[65%] shadow-[0_0_10px_rgba(99,102,241,0.5)]" />
                    </div>
               </div>
               <div className="flex items-center gap-6 text-[10px] font-bold uppercase tracking-widest">
                    <span className="flex items-center gap-2"><div className="w-1.5 h-1.5 rounded-full bg-green-500" /> System: Stable</span>
                    <span className="text-white/60">48kHz / 32bit Float</span>
               </div>
            </div>
          </div>
        </div>
      </main>
      <Toaster position="bottom-right" />
    </div>
  );
}
