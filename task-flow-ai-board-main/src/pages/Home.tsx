import React from 'react';
import { Link } from 'react-router-dom';
import { ArrowRight, Brain, CheckSquare, Target, Zap, Github, Menu } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';

const Home = () => {
  const features = [
    {
      icon: Brain,
      title: 'Intelligent Role Selection',
      description: 'Automatically identifies optimal team roles for your project',
      detail: '50+ specialized roles across all technology domains'
    },
    {
      icon: CheckSquare,
      title: 'Smart Task Generation',
      description: 'Context-aware tasks with technical specifications',
      detail: 'Progressive complexity from foundation to advanced features'
    },
    {
      icon: Target,
      title: 'Kanban Board Interface',
      description: 'Jira-style drag-and-drop task management',
      detail: 'Visual progress tracking across development phases'
    },
    {
      icon: Zap,
      title: 'Instant Analysis',
      description: 'Transform project descriptions into actionable plans in seconds',
      detail: 'Modern tech stack awareness including AI/ML, blockchain, cloud'
    }
  ];

  const projectTypes = [
    { name: 'E-commerce', icon: '🛒', color: 'bg-blue-100 text-blue-800' },
    { name: 'Mobile App', icon: '📱', color: 'bg-green-100 text-green-800' },
    { name: 'AI/ML', icon: '🤖', color: 'bg-purple-100 text-purple-800' },
    { name: 'Blockchain', icon: '⛓️', color: 'bg-orange-100 text-orange-800' },
    { name: 'IoT', icon: '🌐', color: 'bg-cyan-100 text-cyan-800' },
    { name: 'Enterprise', icon: '🏢', color: 'bg-gray-100 text-gray-800' }
  ];

  const roleColors = [
    { role: 'Frontend Developer', color: 'bg-blue-500' },
    { role: 'Backend Developer', color: 'bg-emerald-500' },
    { role: 'AI/ML Engineer', color: 'bg-purple-500' },
    { role: 'DevOps Engineer', color: 'bg-red-500' },
    { role: 'UI/UX Designer', color: 'bg-pink-500' }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50">
      {/* Header */}
      <header className="border-b bg-white/80 backdrop-blur-sm sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center space-x-2">
              <div className="w-8 h-8 bg-gradient-to-br from-blue-600 to-purple-600 rounded-lg flex items-center justify-center">
                <Brain className="w-5 h-5 text-white" />
              </div>
              <span className="text-xl font-bold text-gray-900">Smart Task Agent</span>
            </div>
            
            <nav className="hidden md:flex space-x-8">
              <a href="#" className="text-gray-600 hover:text-gray-900 transition-colors">Home</a>
              <a href="#features" className="text-gray-600 hover:text-gray-900 transition-colors">Features</a>
              <a 
                href="https://github.com/shivansh-2003/Internship_task_roles_allocatement" 
                target="_blank" 
                rel="noopener noreferrer" 
                className="text-gray-600 hover:text-gray-900 transition-colors flex items-center space-x-1"
              >
                <Github className="w-4 h-4" />
                <span>GitHub</span>
              </a>
            </nav>

            <div className="flex items-center space-x-4">
              <Link to="/create">
                <Button className="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700">
                  Try Now
                </Button>
              </Link>
              <Button variant="ghost" size="icon" className="md:hidden">
                <Menu className="w-5 h-5" />
              </Button>
            </div>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto text-center">
          <h1 className="text-4xl md:text-6xl font-bold text-gray-900 mb-6 leading-tight">
            Transform Ideas into
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-purple-600">
              {' '}Actionable Task Breakdowns
            </span>
          </h1>
          
          <p className="text-xl text-gray-600 mb-12 max-w-3xl mx-auto">
            AI-powered project planning that analyzes your requirements and generates 
            role-based task lists instantly
          </p>

          <div className="flex justify-center items-center mb-16">
            <Link to="/create">
              <Button size="lg" className="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-lg px-8 py-3">
                Get Started
                <ArrowRight className="w-5 h-5 ml-2" />
              </Button>
            </Link>
          </div>

          {/* Animated Preview */}
          <div className="relative max-w-4xl mx-auto">
            <div className="bg-white rounded-2xl shadow-2xl border overflow-hidden">
              <div className="bg-gray-50 px-6 py-4 border-b flex items-center space-x-3">
                <div className="flex space-x-2">
                  <div className="w-3 h-3 bg-red-400 rounded-full"></div>
                  <div className="w-3 h-3 bg-yellow-400 rounded-full"></div>
                  <div className="w-3 h-3 bg-green-400 rounded-full"></div>
                </div>
                <span className="text-sm text-gray-600">Smart Task Agent Dashboard</span>
              </div>
              
              <div className="p-6">
                <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                  {['TO DO', 'IN PROGRESS', 'CODE REVIEW', 'DONE'].map((column, idx) => (
                    <div key={column} className="bg-gray-50 rounded-lg p-4">
                      <h3 className="font-semibold text-sm text-gray-700 mb-3">{column}</h3>
                      <div className="space-y-2">
                        {[1, 2].slice(0, idx === 0 ? 2 : idx === 3 ? 1 : 1).map((_, cardIdx) => (
                          <div key={cardIdx} className="bg-white p-3 rounded-lg shadow-sm border">
                            <div className="flex items-center space-x-2 mb-2">
                              <span className={`px-2 py-1 text-xs rounded-full ${roleColors[cardIdx]?.color || 'bg-gray-500'} text-white`}>
                                {roleColors[cardIdx]?.role || 'Developer'}
                              </span>
                            </div>
                            <p className="text-sm text-gray-800">Setup project structure</p>
                          </div>
                        ))}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              Why Choose Smart Task Agent?
            </h2>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              Revolutionize your project planning with AI-powered intelligence
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {features.map((feature, index) => {
              const Icon = feature.icon;
              return (
                <Card key={index} className="group hover:shadow-lg transition-all duration-300 border-0 bg-gradient-to-br from-gray-50 to-white">
                  <CardContent className="p-6">
                    <div className="w-12 h-12 bg-gradient-to-br from-blue-600 to-purple-600 rounded-lg flex items-center justify-center mb-4 group-hover:scale-110 transition-transform duration-300">
                      <Icon className="w-6 h-6 text-white" />
                    </div>
                    <h3 className="text-lg font-semibold text-gray-900 mb-2">{feature.title}</h3>
                    <p className="text-gray-600 mb-2">{feature.description}</p>
                    <p className="text-sm text-blue-600 font-medium">{feature.detail}</p>
                  </CardContent>
                </Card>
              );
            })}
          </div>
        </div>
      </section>

      {/* Technology Showcase */}
      <section className="py-20 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              Supported Project Types
            </h2>
            <p className="text-xl text-gray-600">
              From simple websites to complex AI systems
            </p>
          </div>

          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4 mb-12">
            {projectTypes.map((type, index) => (
              <div key={index} className="bg-white rounded-lg p-4 text-center hover:shadow-md transition-shadow duration-300">
                <div className="text-2xl mb-2">{type.icon}</div>
                <span className={`inline-block px-3 py-1 rounded-full text-sm font-medium ${type.color}`}>
                  {type.name}
                </span>
              </div>
            ))}
          </div>

          <div className="text-center">
            <h3 className="text-xl font-semibold text-gray-900 mb-4">Role-Based Task Organization</h3>
            <div className="flex flex-wrap justify-center gap-3">
              {roleColors.map((item, index) => (
                <span key={index} className={`px-4 py-2 rounded-full text-white font-medium ${item.color}`}>
                  {item.role}
                </span>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-gradient-to-r from-blue-600 to-purple-600">
        <div className="max-w-4xl mx-auto text-center px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl md:text-4xl font-bold text-white mb-6">
            Ready to revolutionize your project planning?
          </h2>
          <p className="text-xl text-blue-100 mb-8">
            Transform your next big idea into a structured, actionable plan in seconds
          </p>
          
          <div className="bg-white/10 backdrop-blur-sm rounded-2xl p-6 mb-8">
            <div className="flex items-center space-x-4">
              <input 
                type="text" 
                placeholder="Describe your project idea..."
                className="flex-1 px-4 py-3 rounded-lg bg-white/20 backdrop-blur-sm text-white placeholder-blue-200 border border-white/30 focus:outline-none focus:ring-2 focus:ring-white/50"
              />
              <Link to="/create">
                <Button className="bg-white text-blue-600 hover:bg-blue-50 px-6 py-3">
                  Generate Tasks
                </Button>
              </Link>
            </div>
          </div>

          <Link to="/create">
            <Button variant="outline" size="lg" className="border-white text-white hover:bg-white hover:text-blue-600">
              Get Started Now
              <ArrowRight className="w-5 h-5 ml-2" />
            </Button>
          </Link>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center">
            <div className="flex items-center space-x-2">
              <div className="w-8 h-8 bg-gradient-to-br from-blue-600 to-purple-600 rounded-lg flex items-center justify-center">
                <Brain className="w-5 h-5 text-white" />
              </div>
              <span className="text-xl font-bold">Smart Task Agent</span>
            </div>
            
            <div className="text-gray-400">
              © 2024 Smart Task Agent. All rights reserved.
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Home;
