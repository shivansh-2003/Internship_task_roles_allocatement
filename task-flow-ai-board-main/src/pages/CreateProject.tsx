import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { ArrowLeft, Sparkles, Loader2, Lightbulb } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { useTask } from '@/contexts/TaskContext';
import { toast } from 'sonner';
import { generateTasks as apiGenerateTasks } from '@/config/api';

const CreateProject = () => {
  const [description, setDescription] = useState('');
  const [isGenerating, setIsGenerating] = useState(false);
  const { dispatch } = useTask();
  const navigate = useNavigate();

  const exampleProjects = [
    {
      title: 'E-commerce Platform with AI Recommendations',
      description: 'Build a modern e-commerce platform with AI-powered product recommendations, user authentication, payment processing, and admin dashboard.'
    },
    {
      title: 'Mobile Fitness App with Social Features',
      description: 'Create a mobile fitness tracking app with workout plans, progress tracking, social features, and integration with wearable devices.'
    },
    {
      title: 'Blockchain DeFi Platform',
      description: 'Develop a decentralized finance platform with smart contracts, yield farming, token swapping, and liquidity mining features.'
    },
    {
      title: 'Enterprise CRM System',
      description: 'Build an enterprise-grade CRM system with lead management, sales pipeline, reporting, and integration with third-party tools.'
    }
  ];

  const generateTasks = async () => {
    if (!description.trim()) {
      toast.error('Please describe your project first');
      return;
    }

    setIsGenerating(true);
    try {
      // Call the real API
      const response = await apiGenerateTasks(description);
      
      // Transform API response to our format
      const tasks = Object.entries(response.role_tasks).flatMap(([role, roleTasks]) =>
        (roleTasks as string[]).map((task, index) => ({
          id: `${role}-${index}`,
          title: task,
          description: `Detailed implementation of: ${task}`,
          role,
          status: 'todo' as const,
          createdAt: new Date(),
          updatedAt: new Date()
        }))
      );

      const project = {
        description,
        generatedAt: new Date(),
        selectedRoles: response.selected_roles,
        tasks
      };

      dispatch({ type: 'SET_PROJECT', payload: project });
      toast.success('Tasks generated successfully!');
      navigate('/board');
      
    } catch (error) {
      console.error('Error generating tasks:', error);
      const errorMessage = error instanceof Error ? error.message : 'Failed to generate tasks. Please try again.';
      toast.error(errorMessage);
    } finally {
      setIsGenerating(false);
    }
  };

  const handleExampleClick = (example: typeof exampleProjects[0]) => {
    setDescription(example.description);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50">
      {/* Header */}
      <header className="border-b bg-white/80 backdrop-blur-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center h-16">
            <Link to="/" className="flex items-center space-x-2 text-gray-600 hover:text-gray-900 transition-colors">
              <ArrowLeft className="w-5 h-5" />
              <span>Back to Home</span>
            </Link>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            Describe Your Project
          </h1>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Tell us about your project idea and we'll generate a comprehensive task breakdown with role assignments
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Main Input Section */}
          <div className="lg:col-span-2">
            <Card className="border-0 shadow-lg">
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Sparkles className="w-5 h-5 text-blue-600" />
                  <span>Project Description</span>
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-6">
                <div className="space-y-2">
                  <Textarea
                    placeholder="Describe your project idea in detail. Include goals, features, technology preferences, and target audience..."
                    value={description}
                    onChange={(e) => setDescription(e.target.value)}
                    rows={12}
                    className="resize-none text-base"
                  />
                  <div className="flex justify-between items-center text-sm text-gray-500">
                    <span>Recommended: 100-500 characters</span>
                    <span>{description.length} characters</span>
                  </div>
                </div>

                <Button
                  onClick={generateTasks}
                  disabled={isGenerating || !description.trim()}
                  className="w-full bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-lg py-6"
                >
                  {isGenerating ? (
                    <>
                      <Loader2 className="w-5 h-5 mr-2 animate-spin" />
                      Analyzing project...
                    </>
                  ) : (
                    <>
                      <Sparkles className="w-5 h-5 mr-2" />
                      Generate Tasks
                    </>
                  )}
                </Button>
              </CardContent>
            </Card>
          </div>

          {/* Examples Sidebar */}
          <div className="space-y-6">
            <Card className="border-0 shadow-lg">
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Lightbulb className="w-5 h-5 text-yellow-600" />
                  <span>Example Projects</span>
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                {exampleProjects.map((example, index) => (
                  <div
                    key={index}
                    onClick={() => handleExampleClick(example)}
                    className="p-4 border rounded-lg cursor-pointer hover:bg-blue-50 hover:border-blue-300 transition-all duration-200"
                  >
                    <h3 className="font-medium text-gray-900 mb-2">{example.title}</h3>
                    <p className="text-sm text-gray-600 line-clamp-3">{example.description}</p>
                  </div>
                ))}
              </CardContent>
            </Card>

            <Card className="border-0 shadow-lg bg-gradient-to-br from-blue-50 to-purple-50">
              <CardContent className="p-6">
                <h3 className="font-semibold text-gray-900 mb-2">💡 Pro Tips</h3>
                <ul className="text-sm text-gray-600 space-y-2">
                  <li>• Be specific about your technology stack</li>
                  <li>• Mention target audience and scale</li>
                  <li>• Include key features and functionality</li>
                  <li>• Specify any constraints or requirements</li>
                </ul>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CreateProject;
