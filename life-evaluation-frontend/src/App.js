import React, { useState, useEffect, useRef } from 'react';
import { Send, Brain, Zap, ArrowRight, Download, Share2, TrendingUp, AlertCircle, Target, Eye, Sparkles, Stars, Atom } from 'lucide-react';

const PsychedelicTruthCanvas = () => {
  const API_BASE = 'http://localhost:8000/api';
  const [userPrompt, setUserPrompt] = useState('');
  const [selectedModel, setSelectedModel] = useState('gpt-4.1-nano');
  const [availableModels, setAvailableModels] = useState({});
  const [phase, setPhase] = useState('input');
  const [questions, setQuestions] = useState([]);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [answers, setAnswers] = useState([]);
  const [currentAnswer, setCurrentAnswer] = useState('');
  const [liveInsights, setLiveInsights] = useState([]);
  const [streamingText, setStreamingText] = useState('');
  const [isStreaming, setIsStreaming] = useState(false);
  const [truthCrystals, setTruthCrystals] = useState([]);
  const [contradictionLightning, setContradictionLightning] = useState([]);
  const [emotionalHeatMap, setEmotionalHeatMap] = useState([]);
  const [particleGalaxy, setParticleGalaxy] = useState([]);
  const [morphingSculpture, setMorphingSculpture] = useState({ shape: 'sphere', intensity: 0, color: '#4f46e5' });
  const [finalAnalysis, setFinalAnalysis] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [selectedQuestionWorld, setSelectedQuestionWorld] = useState(null);
  const canvasRef = useRef(null);
  const resultRef = useRef(null);

  useEffect(() => {
    // Load available models on component mount
    const loadModels = async () => {
      try {
        console.log('Loading models from:', `${API_BASE}/models`);
        const response = await fetch(`${API_BASE}/models`);
        if (!response.ok) {
          throw new Error(`HTTP ${response.status}`);
        }
        const data = await response.json();
        console.log('Models loaded:', data.models);
        setAvailableModels(data.models);
      } catch (error) {
        console.error('Failed to load models:', error);
        // Set default OpenAI models if API fails
        setAvailableModels({
          "gpt-4.1-nano": {
            "name": "GPT-4.1 Nano",
            "price": "$0.10/M tokens",
            "context": "200K",
            "description": "Latest nano model, super cheap and fast"
          },
          "gpt-4o-mini": {
            "name": "GPT-4o Mini", 
            "price": "$0.15/M tokens",
            "context": "128K",
            "description": "Super cheap and fast"
          }
        });
      }
    };
    loadModels();
  }, []);

  const startQuestioning = async () => {
    if (!userPrompt.trim()) return;
    
    setIsLoading(true);
    try {
      const response = await fetch(`${API_BASE}/generate-first-question`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt: userPrompt, model: selectedModel })
      });
      
      const data = await response.json();
      setQuestions([data.question]);
      setPhase('questioning');
      
      // Initialize first question world
      initializeQuestionWorld(0, data.question);
    } catch (error) {
      setQuestions(["Yo, tell me what's really going on with this goal of yours."]);
      setPhase('questioning');
      initializeQuestionWorld(0, "Yo, tell me what's really going on with this goal of yours.");
    } finally {
      setIsLoading(false);
    }
  };

  const initializeQuestionWorld = (index, question) => {
    // Create a new floating world for this question
    const newWorld = {
      id: index,
      question: question,
      answer: null,
      x: 150 + (index * 200),
      y: 300 + Math.sin(index) * 50,
      z: index * 30,
      particles: Array.from({ length: 20 }, (_, i) => ({
        id: i,
        x: Math.random() * 100,
        y: Math.random() * 100,
        speed: Math.random() * 2 + 1,
        size: Math.random() * 5 + 2,
        color: `hsl(${200 + index * 40}, 70%, 60%)`
      })),
      crystalGrowth: 0,
      truthLevel: 0,
      contradictionLevel: 0
    };
    
    setParticleGalaxy(prev => [...prev, newWorld]);
  };

  const generateTruthCrystal = (insight, answerIndex) => {
    const crystalIntensity = insight.includes('truth') || insight.includes('honest') ? 8 : 
                           insight.includes('contradiction') || insight.includes('BS') ? 3 : 5;
    
    const crystal = {
      id: Date.now() + Math.random(),
      x: 100 + (answerIndex * 150) + Math.random() * 100,
      y: 200 + Math.random() * 200,
      size: crystalIntensity * 8,
      intensity: crystalIntensity,
      color: crystalIntensity > 6 ? '#ffd700' : crystalIntensity < 4 ? '#ff4444' : '#4488ff',
      facets: Math.floor(crystalIntensity * 1.5),
      pulsing: true,
      insight: insight,
      answerIndex: answerIndex
    };
    
    setTruthCrystals(prev => [...prev, crystal]);
    
    // Remove after animation
    setTimeout(() => {
      setTruthCrystals(prev => prev.filter(c => c.id !== crystal.id));
    }, 8000);
  };

  const createContradictionLightning = (fromIndex, toIndex, intensity) => {
    const lightning = {
      id: Date.now() + Math.random(),
      fromX: 150 + (fromIndex * 200),
      fromY: 300,
      toX: 150 + (toIndex * 200),
      toY: 300,
      intensity: intensity,
      bolts: Array.from({ length: intensity }, (_, i) => ({
        path: generateLightningPath(150 + (fromIndex * 200), 300, 150 + (toIndex * 200), 300),
        delay: i * 100
      }))
    };
    
    setContradictionLightning(prev => [...prev, lightning]);
    
    setTimeout(() => {
      setContradictionLightning(prev => prev.filter(l => l.id !== lightning.id));
    }, 3000);
  };

  const generateLightningPath = (x1, y1, x2, y2) => {
    const points = [];
    const segments = 8;
    for (let i = 0; i <= segments; i++) {
      const t = i / segments;
      const x = x1 + (x2 - x1) * t + (Math.random() - 0.5) * 30;
      const y = y1 + (y2 - y1) * t + (Math.random() - 0.5) * 30;
      points.push({ x, y });
    }
    return points;
  };

  const updateEmotionalHeatMap = (emotion, intensity, position) => {
    const heatSpot = {
      id: Date.now() + Math.random(),
      x: position.x,
      y: position.y,
      emotion: emotion,
      intensity: intensity,
      radius: intensity * 20,
      color: emotion === 'truth' ? '#00ff88' : 
             emotion === 'lie' ? '#ff4444' : 
             emotion === 'confusion' ? '#ffaa00' : '#8844ff',
      expanding: true
    };
    
    setEmotionalHeatMap(prev => [...prev, heatSpot]);
    
    setTimeout(() => {
      setEmotionalHeatMap(prev => prev.filter(h => h.id !== heatSpot.id));
    }, 5000);
  };

  const morphSculpture = (insight) => {
    const intensity = insight.length / 10;
    const shapes = ['sphere', 'cube', 'pyramid', 'torus', 'crystal'];
    const colors = ['#ff00ff', '#00ffff', '#ffff00', '#ff4444', '#44ff44'];
    
    if (insight.includes('contradiction')) {
      setMorphingSculpture({
        shape: 'tornado',
        intensity: intensity * 2,
        color: '#ff4444'
      });
    } else if (insight.includes('truth')) {
      setMorphingSculpture({
        shape: 'crystal',
        intensity: intensity * 1.5,
        color: '#ffd700'
      });
    } else {
      setMorphingSculpture({
        shape: shapes[Math.floor(Math.random() * shapes.length)],
        intensity: intensity,
        color: colors[Math.floor(Math.random() * colors.length)]
      });
    }
  };

  const submitAnswer = async () => {
    if (!currentAnswer.trim()) return;
    
    const newAnswers = [...answers, currentAnswer];
    setAnswers(newAnswers);
    setIsLoading(true);

    // Update the current question world with the answer
    setParticleGalaxy(prev => prev.map((world, index) => 
      index === currentQuestionIndex 
        ? { ...world, answer: currentAnswer, crystalGrowth: 50 }
        : world
    ));

    try {
      const response = await fetch(`${API_BASE}/analyze-answer-bro`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          prompt: userPrompt,
          questions: questions,
          answers: newAnswers,
          current_answer: currentAnswer,
          model: selectedModel
        })
      });
      
      const data = await response.json();
      
      // VISUAL EFFECTS EXPLOSION! 🎆
      generateTruthCrystal(data.analysis, currentQuestionIndex);
      morphSculpture(data.analysis);
      updateEmotionalHeatMap(
        data.analysis.includes('BS') ? 'lie' : 'truth', 
        Math.random() * 5 + 3,
        { x: 400 + Math.random() * 200, y: 200 + Math.random() * 200 }
      );

      // Check for contradictions with previous answers
      if (currentQuestionIndex > 0 && data.analysis.includes('contradiction')) {
        createContradictionLightning(0, currentQuestionIndex, 3);
      }

      // Stream the analysis
      await streamAnalysis(data.analysis);
      setLiveInsights(prev => [...prev, data.analysis]);

      // Generate next question if not done
      if (newAnswers.length < 5) {
        const nextResponse = await fetch(`${API_BASE}/generate-next-question-bro`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            prompt: userPrompt,
            questions: questions,
            answers: newAnswers,
            model: selectedModel
          })
        });
        
        const nextData = await nextResponse.json();
        setQuestions(prev => [...prev, nextData.question]);
        setCurrentQuestionIndex(currentQuestionIndex + 1);
        
        // Create next question world
        initializeQuestionWorld(currentQuestionIndex + 1, nextData.question);
      } else {
        // Final explosion of effects!
        for (let i = 0; i < 5; i++) {
          setTimeout(() => {
            generateTruthCrystal("FINAL ANALYSIS COMPLETE! 🎯", i);
          }, i * 200);
        }
        await generateFinalAnalysis(newAnswers);
      }
      
    } catch (error) {
      const fallback = `Hmm, that's sus... 🤔 I'm seeing some interesting patterns here.`;
      await streamAnalysis(fallback);
      setLiveInsights(prev => [...prev, fallback]);
      
      if (newAnswers.length < 5) {
        setQuestions(prev => [...prev, "Tell me more, I'm not convinced yet."]);
        setCurrentQuestionIndex(currentQuestionIndex + 1);
        initializeQuestionWorld(currentQuestionIndex + 1, "Tell me more, I'm not convinced yet.");
      }
    } finally {
      setCurrentAnswer('');
      setIsLoading(false);
    }
  };

  const streamAnalysis = async (text) => {
    setIsStreaming(true);
    setStreamingText('');
    
    for (let i = 0; i < text.length; i++) {
      await new Promise(resolve => setTimeout(resolve, 30));
      setStreamingText(text.slice(0, i + 1));
    }
    setIsStreaming(false);
  };

  const generateFinalAnalysis = async (allAnswers) => {
    try {
      const response = await fetch(`${API_BASE}/generate-final-roast`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          prompt: userPrompt,
          questions: questions,
          answers: allAnswers,
          model: selectedModel
        })
      });
      
      const data = await response.json();
      setFinalAnalysis(data);
      setPhase('results');
    } catch (error) {
      setFinalAnalysis({
        title: "The Cosmic Truth Report 🌌",
        summary: "After diving deep into your reality matrix...",
        insights: ["Your potential is off the charts", "Some patterns need rewiring", "The universe is ready for your next move"]
      });
      setPhase('results');
    }
  };

  const reset = () => {
    setUserPrompt('');
    setPhase('input');
    setQuestions([]);
    setCurrentQuestionIndex(0);
    setAnswers([]);
    setCurrentAnswer('');
    setLiveInsights([]);
    setStreamingText('');
    setTruthCrystals([]);
    setContradictionLightning([]);
    setEmotionalHeatMap([]);
    setParticleGalaxy([]);
    setMorphingSculpture({ shape: 'sphere', intensity: 0, color: '#4f46e5' });
    setFinalAnalysis(null);
    setIsLoading(false);
    setSelectedQuestionWorld(null);
  };

  if (phase === 'input') {
    return (
      <div className="min-h-screen bg-gradient-to-br from-purple-900 via-blue-900 to-indigo-900 p-4 relative overflow-hidden">
        {/* Cosmic background animation */}
        <div className="absolute inset-0">
          {[...Array(100)].map((_, i) => (
            <div
              key={i}
              className="absolute w-1 h-1 bg-white rounded-full animate-pulse"
              style={{
                left: `${Math.random() * 100}%`,
                top: `${Math.random() * 100}%`,
                animationDelay: `${Math.random() * 5}s`,
                animationDuration: `${1 + Math.random() * 4}s`,
                opacity: Math.random() * 0.8 + 0.2
              }}
            />
          ))}
        </div>
        
        {/* Floating geometric shapes */}
        <div className="absolute inset-0">
          {[...Array(20)].map((_, i) => (
            <div
              key={i}
              className="absolute"
              style={{
                left: `${Math.random() * 100}%`,
                top: `${Math.random() * 100}%`,
                animation: `float ${5 + Math.random() * 5}s ease-in-out infinite`,
                animationDelay: `${Math.random() * 3}s`
              }}
            >
              <div 
                className={`w-8 h-8 ${Math.random() > 0.5 ? 'rounded-full' : 'rotate-45'} bg-gradient-to-r ${
                  ['from-pink-500 to-violet-500', 'from-cyan-500 to-blue-500', 'from-green-500 to-teal-500'][Math.floor(Math.random() * 3)]
                } opacity-20`}
              />
            </div>
          ))}
        </div>

        <div className="relative max-w-4xl mx-auto pt-20">
          <div className="text-center mb-16">
            <div className="text-9xl mb-8 animate-bounce">🌌</div>
            <h1 className="text-7xl font-black text-white mb-6 tracking-wider">
              REALITY
              <span className="bg-gradient-to-r from-pink-400 via-purple-500 to-cyan-400 bg-clip-text text-transparent animate-pulse">
                {" "}SCANNER
              </span>
            </h1>
            <p className="text-3xl text-purple-200 mb-12 font-light leading-relaxed">
              I'll map your truth in 5D space with psychedelic visualizations 🎨✨
            </p>
          </div>

          <div className="bg-black/30 backdrop-blur-2xl rounded-3xl shadow-2xl p-12 border-2 border-purple-500/30 relative overflow-hidden">
            {/* Animated border effect */}
            <div className="absolute inset-0 rounded-3xl bg-gradient-to-r from-pink-500 via-purple-500 to-cyan-500 opacity-20 animate-pulse"></div>
            
            <div className="relative">
              <label className="block text-3xl font-bold text-white mb-8 text-center">
                What reality needs scanning? 🎯
              </label>
              
              {/* Model Selector */}
              <div className="mb-6">
                <label className="block text-lg font-semibold text-purple-200 mb-3">
                  Choose Your AI Model 🤖 (All FREE!)
                </label>
                <select
                  value={selectedModel}
                  onChange={(e) => setSelectedModel(e.target.value)}
                  className="w-full p-4 bg-white/10 border-2 border-purple-400/50 rounded-xl text-white outline-none focus:border-cyan-400 focus:ring-2 focus:ring-cyan-400/20 backdrop-blur-sm"
                >
                  {Object.entries(availableModels).map(([key, model]) => (
                    <option key={key} value={key} className="bg-gray-800 text-white">
                      {model.name} ({model.context}) - {model.description}
                    </option>
                  ))}
                </select>
                <div className="flex flex-wrap gap-2 mt-3">
                  <span className="text-xs bg-green-500/20 text-green-300 px-3 py-1 rounded-full">
                    💡 GPT-4o Mini is super cheap at $0.15/M tokens
                  </span>
                  <span className="text-xs bg-blue-500/20 text-blue-300 px-3 py-1 rounded-full">
                    🚀 GPT-4o for premium roasting
                  </span>
                  <span className="text-xs bg-purple-500/20 text-purple-300 px-3 py-1 rounded-full">
                    🧠 All models have great context!
                  </span>
                </div>
              </div>

              <input
                type="text"
                value={userPrompt}
                onChange={(e) => setUserPrompt(e.target.value)}
                placeholder="get a girlfriend, start a business, get jacked, find purpose..."
                className="w-full p-8 bg-white/10 border-2 border-purple-400/50 rounded-2xl text-2xl text-white placeholder-purple-300 focus:border-cyan-400 focus:ring-4 focus:ring-cyan-400/20 outline-none transition-all backdrop-blur-sm font-medium"
                onKeyPress={(e) => e.key === 'Enter' && startQuestioning()}
              />
              <button
                onClick={startQuestioning}
                disabled={!userPrompt.trim() || isLoading}
                className="w-full mt-8 bg-gradient-to-r from-pink-600 via-purple-600 to-cyan-600 text-white py-8 px-12 rounded-2xl text-2xl font-black hover:from-pink-700 hover:via-purple-700 hover:to-cyan-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all transform hover:scale-105 shadow-2xl relative overflow-hidden"
              >
                <div className="absolute inset-0 bg-gradient-to-r from-pink-500 to-cyan-500 opacity-0 hover:opacity-20 transition-opacity"></div>
                <span className="relative">
                  {isLoading ? '🌀 INITIALIZING TRUTH MATRIX...' : '🚀 ENTER THE MATRIX'}
                </span>
              </button>
            </div>
          </div>
        </div>

        <style jsx>{`
          @keyframes float {
            0%, 100% { transform: translateY(0px) rotate(0deg); }
            50% { transform: translateY(-20px) rotate(180deg); }
          }
        `}</style>
      </div>
    );
  }

  if (phase === 'questioning') {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-indigo-900 relative overflow-hidden">
        {/* Cosmic Canvas Background */}
        <canvas 
          ref={canvasRef}
          className="absolute inset-0 pointer-events-none"
          width="1920"
          height="1080"
        />

        {/* Truth Crystals */}
        {truthCrystals.map(crystal => (
          <div
            key={crystal.id}
            className="absolute pointer-events-none z-40"
            style={{ 
              left: `${crystal.x}px`, 
              top: `${crystal.y}px`,
              transform: 'translate(-50%, -50%)'
            }}
          >
            <div 
              className="relative animate-pulse"
              style={{
                width: `${crystal.size}px`,
                height: `${crystal.size}px`,
                background: `radial-gradient(circle, ${crystal.color}40, ${crystal.color}80, ${crystal.color}FF)`,
                clipPath: 'polygon(50% 0%, 0% 100%, 100% 100%)',
                filter: 'drop-shadow(0 0 20px ' + crystal.color + ')',
                animation: crystal.pulsing ? 'crystalPulse 2s ease-in-out infinite' : 'none'
              }}
            >
              {/* Crystal facets */}
              {[...Array(crystal.facets)].map((_, i) => (
                <div
                  key={i}
                  className="absolute inset-0 opacity-30"
                  style={{
                    background: `linear-gradient(${i * (360/crystal.facets)}deg, transparent, ${crystal.color}80)`,
                    clipPath: 'polygon(50% 0%, 0% 100%, 100% 100%)'
                  }}
                />
              ))}
            </div>
            
            {/* Crystal insight tooltip */}
            <div className="absolute top-full left-1/2 transform -translate-x-1/2 mt-2 bg-black/80 text-white text-xs p-2 rounded whitespace-nowrap">
              {crystal.insight.slice(0, 30)}...
            </div>
          </div>
        ))}

        {/* Contradiction Lightning */}
        {contradictionLightning.map(lightning => (
          <svg
            key={lightning.id}
            className="absolute inset-0 pointer-events-none z-30"
            width="100%"
            height="100%"
          >
            {lightning.bolts.map((bolt, i) => (
              <g key={i}>
                <path
                  d={`M ${bolt.path.map(p => `${p.x},${p.y}`).join(' L ')}`}
                  stroke="#ff4444"
                  strokeWidth={Math.random() * 3 + 1}
                  fill="none"
                  opacity="0.8"
                  style={{
                    filter: 'drop-shadow(0 0 10px #ff4444)',
                    animation: `lightning 0.1s ease-in-out ${bolt.delay}ms`
                  }}
                />
              </g>
            ))}
          </svg>
        ))}

        {/* Emotional Heat Map */}
        {emotionalHeatMap.map(spot => (
          <div
            key={spot.id}
            className="absolute pointer-events-none z-20"
            style={{
              left: `${spot.x}px`,
              top: `${spot.y}px`,
              width: `${spot.radius * 2}px`,
              height: `${spot.radius * 2}px`,
              transform: 'translate(-50%, -50%)',
              background: `radial-gradient(circle, ${spot.color}60, ${spot.color}20, transparent)`,
              borderRadius: '50%',
              animation: spot.expanding ? 'heatExpand 3s ease-out forwards' : 'none'
            }}
          />
        ))}

        {/* Morphing Sculpture */}
        <div className="absolute top-20 right-20 z-50">
          <div 
            className="relative w-32 h-32"
            style={{
              background: `radial-gradient(circle, ${morphingSculpture.color}40, ${morphingSculpture.color}80)`,
              borderRadius: morphingSculpture.shape === 'sphere' ? '50%' : 
                          morphingSculpture.shape === 'cube' ? '10%' : '20%',
              transform: `scale(${1 + morphingSculpture.intensity * 0.3}) rotate(${morphingSculpture.intensity * 45}deg)`,
              filter: `drop-shadow(0 0 ${morphingSculpture.intensity * 10}px ${morphingSculpture.color})`,
              animation: 'morph 3s ease-in-out infinite'
            }}
          >
            <div className="absolute inset-2 bg-white/20 rounded-full animate-spin" />
            <div className="absolute inset-4 bg-white/40 rounded-full animate-pulse" />
          </div>
        </div>

        <div className="relative z-10 p-6">
          {/* Floating Question Worlds Timeline */}
          <div className="mb-8">
            <h2 className="text-center text-2xl font-bold text-white mb-4">🌍 QUESTION WORLDS 🌍</h2>
            <div className="relative h-64 overflow-x-auto">
              <div className="flex space-x-8 p-4 min-w-max">
                {particleGalaxy.map((world, index) => (
                  <div
                    key={world.id}
                    className={`relative cursor-pointer transition-all duration-500 transform hover:scale-110 ${
                      selectedQuestionWorld === index ? 'scale-125' : ''
                    }`}
                    onClick={() => setSelectedQuestionWorld(selectedQuestionWorld === index ? null : index)}
                    style={{
                      transform: `translateZ(${world.z}px) translateY(${Math.sin(Date.now() * 0.001 + index) * 10}px)`
                    }}
                  >
                    {/* World Sphere */}
                    <div 
                      className="w-40 h-40 rounded-full relative overflow-hidden border-4 border-white/30"
                      style={{
                        background: index <= currentQuestionIndex 
                          ? `radial-gradient(circle, ${world.particles[0]?.color || '#4f46e5'}60, ${world.particles[0]?.color || '#4f46e5'}20)`
                          : 'radial-gradient(circle, #333, #111)',
                        boxShadow: index <= currentQuestionIndex 
                          ? `0 0 30px ${world.particles[0]?.color || '#4f46e5'}80`
                          : '0 0 10px #333'
                      }}
                    >
                      {/* Floating Particles */}
                      {world.particles.map(particle => (
                        <div
                          key={particle.id}
                          className="absolute rounded-full animate-pulse"
                          style={{
                            width: `${particle.size}px`,
                            height: `${particle.size}px`,
                            backgroundColor: particle.color,
                            left: `${particle.x}%`,
                            top: `${particle.y}%`,
                            animation: `float ${particle.speed}s ease-in-out infinite`,
                            animationDelay: `${particle.id * 0.1}s`
                          }}
                        />
                      ))}

                      {/* Crystal Growth */}
                      {world.crystalGrowth > 0 && (
                        <div 
                          className="absolute inset-0 rounded-full"
                          style={{
                            background: `conic-gradient(from 0deg, transparent, #ffd70060, transparent)`,
                            animation: 'spin 2s linear infinite'
                          }}
                        />
                      )}

                      {/* World Number */}
                      <div className="absolute inset-0 flex items-center justify-center">
                        <div className="text-3xl font-black text-white bg-black/50 rounded-full w-12 h-12 flex items-center justify-center">
                          {index + 1}
                        </div>
                      </div>
                    </div>

                    {/* World Info */}
                    <div className="absolute -bottom-16 left-1/2 transform -translate-x-1/2 text-center w-48">
                      <div className={`text-sm font-bold mb-1 ${
                        index <= currentQuestionIndex ? 'text-cyan-300' : 'text-gray-500'
                      }`}>
                        {index < currentQuestionIndex ? '✅ ANSWERED' : 
                         index === currentQuestionIndex ? '🎯 CURRENT' : '⏳ PENDING'}
                      </div>
                      <div className="text-xs text-white/80 leading-tight">
                        {world.question.slice(0, 50)}...
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Expanded Question World View */}
          {selectedQuestionWorld !== null && (
            <div className="mb-8 bg-black/60 backdrop-blur-xl rounded-3xl p-6 border border-cyan-500/30">
              <div className="text-center mb-4">
                <h3 className="text-2xl font-bold text-cyan-300">🌍 WORLD {selectedQuestionWorld + 1} DETAILS</h3>
              </div>
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <div>
                  <h4 className="text-lg font-bold text-white mb-2">📝 QUESTION:</h4>
                  <p className="text-purple-200 bg-purple-900/30 p-4 rounded-xl">
                    {particleGalaxy[selectedQuestionWorld]?.question}
                  </p>
                </div>
                {particleGalaxy[selectedQuestionWorld]?.answer && (
                  <div>
                    <h4 className="text-lg font-bold text-white mb-2">💭 YOUR ANSWER:</h4>
                    <p className="text-green-200 bg-green-900/30 p-4 rounded-xl">
                      {particleGalaxy[selectedQuestionWorld]?.answer}
                    </p>
                  </div>
                )}
              </div>
            </div>
          )}

          {/* Current Question Interface */}
          {currentQuestionIndex < questions.length && answers.length < 5 && (
            <div className="max-w-4xl mx-auto">
              <div className="bg-black/60 backdrop-blur-xl rounded-3xl shadow-2xl p-8 border border-purple-500/30 relative overflow-hidden">
                {/* Animated background patterns */}
                <div className="absolute inset-0 opacity-10">
                  <div className="absolute inset-0 bg-gradient-to-r from-purple-500 via-pink-500 to-cyan-500 animate-pulse"></div>
                  {[...Array(20)].map((_, i) => (
                    <div
                      key={i}
                      className="absolute w-2 h-2 bg-white rounded-full animate-ping"
                      style={{
                        left: `${Math.random() * 100}%`,
                        top: `${Math.random() * 100}%`,
                        animationDelay: `${Math.random() * 2}s`,
                        animationDuration: `${1 + Math.random() * 2}s`
                      }}
                    />
                  ))}
                </div>

                <div className="relative z-10">
                  <div className="text-center mb-8">
                    <div className="text-6xl mb-4 animate-bounce">🎯</div>
                    <h2 className="text-3xl font-bold text-white mb-6">
                      REALITY PROBE {currentQuestionIndex + 1}/5
                    </h2>
                    <div className="bg-gradient-to-r from-purple-600 to-cyan-600 text-white p-6 rounded-2xl text-xl leading-relaxed font-medium">
                      {questions[currentQuestionIndex]}
                    </div>
                  </div>
                  
                  <div className="space-y-6">
                    <textarea
                      value={currentAnswer}
                      onChange={(e) => setCurrentAnswer(e.target.value)}
                      placeholder="Unleash your truth into the cosmos... 🌌"
                      className="w-full h-40 p-6 bg-white/10 border-2 border-purple-400/50 rounded-2xl text-lg text-white placeholder-purple-300 outline-none focus:border-cyan-400 focus:ring-4 focus:ring-cyan-400/20 resize-none transition-all backdrop-blur-sm"
                      style={{
                        fontFamily: 'inherit',
                        lineHeight: '1.6'
                      }}
                    />
                    
                    <button
                      onClick={submitAnswer}
                      disabled={!currentAnswer.trim() || isLoading}
                      className="w-full bg-gradient-to-r from-green-600 via-blue-600 to-purple-600 text-white py-6 px-8 rounded-2xl text-xl font-bold hover:from-green-700 hover:via-blue-700 hover:to-purple-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all transform hover:scale-105 flex items-center justify-center gap-3 relative overflow-hidden"
                    >
                      {/* Button animation overlay */}
                      <div className="absolute inset-0 bg-gradient-to-r from-pink-500 to-cyan-500 opacity-0 hover:opacity-20 transition-opacity"></div>
                      
                      <span className="relative flex items-center gap-3">
                        {isLoading ? (
                          <>
                            <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-white"></div>
                            SCANNING REALITY MATRIX...
                          </>
                        ) : (
                          <>
                            🚀 LAUNCH INTO TRUTH SPACE
                            <ArrowRight className="w-6 h-6" />
                          </>
                        )}
                      </span>
                    </button>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Live Analysis Stream */}
          <div className="max-w-4xl mx-auto mt-8">
            <div className="bg-black/60 backdrop-blur-xl rounded-3xl shadow-2xl p-6 border border-yellow-500/30">
              <div className="flex items-center gap-3 mb-6">
                <Zap className="w-8 h-8 text-yellow-400 animate-pulse" />
                <h3 className="text-2xl font-bold text-white">🔥 LIVE TRUTH ANALYSIS</h3>
                <Sparkles className="w-6 h-6 text-cyan-400 animate-spin" />
              </div>
              
              {liveInsights.length === 0 && !isStreaming ? (
                <div className="text-center py-12">
                  <div className="text-6xl mb-4 animate-pulse">👁️</div>
                  <p className="text-purple-300 text-lg">The cosmic truth scanner is calibrated and ready...</p>
                </div>
              ) : (
                <div className="space-y-4 max-h-80 overflow-y-auto">
                  {liveInsights.map((insight, index) => (
                    <div 
                      key={index} 
                      className="relative bg-gradient-to-r from-yellow-900/50 to-red-900/50 border-l-4 border-yellow-400 p-6 rounded-xl transform transition-all duration-500 hover:scale-105"
                      style={{
                        animation: `slideInLeft 0.5s ease-out ${index * 0.1}s both`
                      }}
                    >
                      {/* Particle effects around insight */}
                      <div className="absolute -top-2 -right-2 w-4 h-4 bg-yellow-400 rounded-full animate-ping"></div>
                      <div className="absolute -bottom-2 -left-2 w-3 h-3 bg-cyan-400 rounded-full animate-pulse"></div>
                      
                      <div className="flex items-start gap-3">
                        <div className="text-3xl">{['🎯', '🧐', '🔍', '💡', '🔥'][index] || '💭'}</div>
                        <div>
                          <p className="text-yellow-300 text-sm font-bold mb-2 uppercase tracking-wide">
                            REALITY SCAN #{index + 1}
                          </p>
                          <p className="text-white text-lg leading-relaxed">{insight}</p>
                        </div>
                      </div>
                    </div>
                  ))}
                  
                  {isStreaming && (
                    <div className="bg-gradient-to-r from-purple-900/50 to-blue-900/50 border-l-4 border-blue-400 p-6 rounded-xl">
                      <div className="flex items-start gap-3">
                        <div className="text-3xl animate-spin">🌀</div>
                        <div>
                          <p className="text-blue-300 text-sm font-bold mb-2 uppercase tracking-wide">
                            PROCESSING TRUTH PATTERNS...
                          </p>
                          <p className="text-white text-lg leading-relaxed">
                            {streamingText}
                            <span className="animate-pulse text-cyan-400">|</span>
                          </p>
                        </div>
                      </div>
                    </div>
                  )}
                </div>
              )}
            </div>
          </div>
        </div>

        <style jsx>{`
          @keyframes crystalPulse {
            0%, 100% { transform: scale(1) rotate(0deg); filter: brightness(1); }
            50% { transform: scale(1.2) rotate(180deg); filter: brightness(1.5); }
          }
          
          @keyframes lightning {
            0% { opacity: 0; }
            10% { opacity: 1; }
            20% { opacity: 0; }
            30% { opacity: 1; }
            40% { opacity: 0; }
            100% { opacity: 0; }
          }
          
          @keyframes heatExpand {
            0% { transform: translate(-50%, -50%) scale(0); opacity: 0.8; }
            100% { transform: translate(-50%, -50%) scale(2); opacity: 0; }
          }
          
          @keyframes morph {
            0% { border-radius: 50%; }
            25% { border-radius: 20%; transform: scale(1.1) rotate(90deg); }
            50% { border-radius: 0%; transform: scale(0.9) rotate(180deg); }
            75% { border-radius: 20%; transform: scale(1.1) rotate(270deg); }
            100% { border-radius: 50%; transform: scale(1) rotate(360deg); }
          }
          
          @keyframes slideInLeft {
            0% { transform: translateX(-100%) scale(0.8); opacity: 0; }
            100% { transform: translateX(0%) scale(1); opacity: 1; }
          }
          
          @keyframes spin {
            from { transform: rotate(0deg); }
            to { transform: rotate(360deg); }
          }
        `}</style>
      </div>
    );
  }

  if (phase === 'results') {
    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-indigo-900 p-4 relative overflow-hidden">
        {/* Cosmic celebration background */}
        <div className="absolute inset-0">
          {[...Array(50)].map((_, i) => (
            <div
              key={i}
              className="absolute animate-ping"
              style={{
                left: `${Math.random() * 100}%`,
                top: `${Math.random() * 100}%`,
                animationDelay: `${Math.random() * 3}s`,
                animationDuration: `${1 + Math.random() * 2}s`
              }}
            >
              <div className="w-2 h-2 bg-gradient-to-r from-yellow-400 to-pink-500 rounded-full"></div>
            </div>
          ))}
        </div>

        <div className="relative max-w-6xl mx-auto pt-8">
          <div className="text-center mb-12">
            <div className="text-8xl mb-6 animate-bounce">🎯</div>
            <h1 className="text-6xl font-black text-white mb-4">
              COSMIC TRUTH REPORT
            </h1>
            <p className="text-2xl text-purple-300">Your reality has been fully scanned and analyzed...</p>
          </div>

          <div ref={resultRef} className="bg-black/80 backdrop-blur-xl rounded-3xl shadow-2xl p-8 border border-purple-500/30 relative overflow-hidden">
            {/* Animated result background */}
            <div className="absolute inset-0 opacity-5">
              <div className="absolute inset-0 bg-gradient-to-r from-pink-500 via-purple-500 to-cyan-500 animate-pulse"></div>
            </div>

            {finalAnalysis && (
              <div className="relative space-y-8">
                <div className="text-center">
                  <h2 className="text-4xl font-bold text-white mb-6">{finalAnalysis.title}</h2>
                  <div className="bg-gradient-to-r from-purple-600 to-cyan-600 text-white p-6 rounded-2xl text-xl leading-relaxed">
                    {finalAnalysis.summary}
                  </div>
                </div>

                {/* Question World Summary */}
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                  {particleGalaxy.slice(0, answers.length).map((world, index) => (
                    <div key={index} className="bg-white/10 rounded-2xl p-6 border border-cyan-400/30">
                      <div className="text-center mb-4">
                        <div className="text-3xl mb-2">🌍</div>
                        <h3 className="text-lg font-bold text-cyan-300">WORLD {index + 1}</h3>
                      </div>
                      <div className="space-y-3">
                        <div>
                          <p className="text-xs text-gray-400 font-medium mb-1">QUESTION:</p>
                          <p className="text-white text-sm leading-tight">{world.question}</p>
                        </div>
                        <div>
                          <p className="text-xs text-gray-400 font-medium mb-1">YOUR TRUTH:</p>
                          <p className="text-green-300 text-sm leading-tight">{world.answer}</p>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>

                {/* Live Roast Archive - All the funny shit */}
                {liveInsights.length > 0 && (
                  <div className="bg-gradient-to-r from-yellow-900/50 to-red-900/50 rounded-2xl p-8 border border-yellow-400/30 mb-8">
                    <h3 className="text-3xl font-bold text-white mb-6 text-center flex items-center justify-center gap-3">
                      <Zap className="w-8 h-8 text-yellow-400" />
                      🔥 LIVE ROAST ARCHIVE 🔥
                      <Sparkles className="w-8 h-8 text-cyan-400" />
                    </h3>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      {liveInsights.map((roast, index) => (
                        <div 
                          key={index} 
                          className="bg-black/40 rounded-xl p-4 border border-yellow-400/20 transform transition-all duration-300 hover:scale-105"
                        >
                          <div className="flex items-start gap-3">
                            <div className="text-2xl">{['🎯', '🧐', '🔍', '💡', '🔥'][index] || '💭'}</div>
                            <div>
                              <p className="text-yellow-300 text-xs font-bold mb-2 uppercase tracking-wide">
                                ROAST #{index + 1}
                              </p>
                              <p className="text-white leading-relaxed">{roast}</p>
                            </div>
                          </div>
                        </div>
                      ))}
                    </div>
                    <div className="text-center mt-6">
                      <div className="inline-flex items-center gap-2 bg-yellow-500/20 text-yellow-300 px-4 py-2 rounded-full">
                        <span className="text-lg">😂</span>
                        <span className="font-medium">Your journey through truth and roasts</span>
                        <span className="text-lg">😂</span>
                      </div>
                    </div>
                  </div>
                )}
                {finalAnalysis.insights && finalAnalysis.insights.length > 0 && (
                  <div className="bg-purple-900/50 rounded-2xl p-8 border border-pink-400/30">
                    <h3 className="text-3xl font-bold text-white mb-8 text-center flex items-center justify-center gap-3">
                      <Sparkles className="w-8 h-8 text-pink-400" />
                      🔥 COSMIC INSIGHTS
                      <Stars className="w-8 h-8 text-cyan-400" />
                    </h3>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                      {finalAnalysis.insights.map((insight, index) => (
                        <div 
                          key={index} 
                          className="bg-gradient-to-r from-pink-900/50 to-purple-900/50 rounded-xl p-6 border border-pink-400/20 transform transition-all duration-300 hover:scale-105 hover:border-pink-400/50"
                        >
                          <div className="flex items-start gap-4">
                            <div className="text-4xl">{['💎', '🎯', '⚡', '🔮', '🌟'][index] || '💭'}</div>
                            <div>
                              <p className="text-pink-300 text-sm font-bold mb-2 uppercase tracking-wide">
                                INSIGHT #{index + 1}
                              </p>
                              <p className="text-white text-lg leading-relaxed">{insight}</p>
                            </div>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                <div className="flex gap-6 justify-center">
                  <button
                    onClick={() => alert('Screenshot this cosmic report! 📸')}
                    className="bg-gradient-to-r from-green-600 to-cyan-600 hover:from-green-700 hover:to-cyan-700 text-white py-4 px-8 rounded-xl text-lg font-bold flex items-center gap-3 transition-all transform hover:scale-105 shadow-lg"
                  >
                    <Download className="w-6 h-6" />
                    SAVE COSMIC REPORT
                  </button>
                  <button
                    onClick={reset}
                    className="bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white py-4 px-8 rounded-xl text-lg font-bold flex items-center gap-3 transition-all transform hover:scale-105 shadow-lg"
                  >
                    <Atom className="w-6 h-6" />
                    SCAN NEW REALITY
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    );
  }
};

export default PsychedelicTruthCanvas;