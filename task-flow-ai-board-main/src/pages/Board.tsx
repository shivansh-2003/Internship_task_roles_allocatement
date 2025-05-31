import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { 
  ArrowLeft, 
  Search, 
  Download, 
  Plus,
  Users,
  Clock,
  BarChart3
} from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import { useTask } from '@/contexts/TaskContext';
import { KanbanBoard } from '@/components/KanbanBoard';
import { toast } from 'sonner';

const Board = () => {
  const { state, dispatch } = useTask();
  const navigate = useNavigate();
  const [searchTerm, setSearchTerm] = useState('');

  if (!state.currentProject) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50 flex items-center justify-center">
        <div className="text-center">
          <h1 className="text-2xl font-bold text-gray-900 mb-4">No Project Found</h1>
          <p className="text-gray-600 mb-6">Please create a project first</p>
          <Link to="/create">
            <Button>Create Project</Button>
          </Link>
        </div>
      </div>
    );
  }

  const { currentProject, columns } = state;
  const totalTasks = Object.values(columns).reduce((sum, tasks) => sum + tasks.length, 0);
  const completedTasks = columns.done.length;
  const progressPercentage = totalTasks > 0 ? (completedTasks / totalTasks) * 100 : 0;

  const roleColors: Record<string, string> = {
    'Frontend Developer': 'bg-blue-500',
    'Backend Developer': 'bg-emerald-500',
    'AI/ML Engineer': 'bg-purple-500',
    'Database Specialist': 'bg-amber-500',
    'DevOps Engineer': 'bg-red-500',
    'UI/UX Designer': 'bg-pink-500',
    'Security Engineer': 'bg-gray-500',
    'Product Manager': 'bg-lime-500',
    'Quality Assurance': 'bg-cyan-500',
    'Blockchain Developer': 'bg-orange-500'
  };

  const handleNewProject = () => {
    dispatch({ type: 'RESET_PROJECT' });
    navigate('/create');
  };

  const handleExportTasks = () => {
    const data = {
      project: currentProject,
      tasks: Object.values(columns).flat()
    };
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'project-tasks.json';
    a.click();
    URL.revokeObjectURL(url);
    toast.success('Tasks exported successfully!');
  };

  const roleTaskCounts = currentProject.selectedRoles.reduce((acc, role) => {
    acc[role] = Object.values(columns).flat().filter(task => task.role === role).length;
    return acc;
  }, {} as Record<string, number>);

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50">
      {/* Header */}
      <header className="border-b bg-white/80 backdrop-blur-sm sticky top-0 z-40">
        <div className="max-w-full px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center space-x-4">
              <Link to="/" className="flex items-center space-x-2 text-gray-600 hover:text-gray-900 transition-colors">
                <ArrowLeft className="w-5 h-5" />
                <span>Home</span>
              </Link>
              <div className="h-6 w-px bg-gray-300"></div>
              <h1 className="text-lg font-semibold text-gray-900">Project Board</h1>
            </div>

            <div className="flex items-center space-x-3">
              <div className="relative">
                <Search className="w-4 h-4 absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
                <Input
                  placeholder="Search tasks..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="pl-10 w-64"
                />
              </div>
              
              <Button variant="outline" size="sm" onClick={handleExportTasks}>
                <Download className="w-4 h-4 mr-2" />
                Export
              </Button>
              
              <Button onClick={handleNewProject} className="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700">
                <Plus className="w-4 h-4 mr-2" />
                New Project
              </Button>
            </div>
          </div>
        </div>
      </header>

      <div className="flex">
        {/* Main Board Area */}
        <div className="flex-1 p-6">
          {/* Project Stats */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
            <Card>
              <CardContent className="p-4">
                <div className="flex items-center space-x-2">
                  <BarChart3 className="w-5 h-5 text-blue-600" />
                  <div>
                    <p className="text-sm text-gray-600">Total Tasks</p>
                    <p className="text-2xl font-bold text-gray-900">{totalTasks}</p>
                  </div>
                </div>
              </CardContent>
            </Card>
            
            <Card>
              <CardContent className="p-4">
                <div className="flex items-center space-x-2">
                  <Clock className="w-5 h-5 text-green-600" />
                  <div>
                    <p className="text-sm text-gray-600">Completed</p>
                    <p className="text-2xl font-bold text-gray-900">{completedTasks}</p>
                  </div>
                </div>
              </CardContent>
            </Card>
            
            <Card>
              <CardContent className="p-4">
                <div className="flex items-center space-x-2">
                  <Users className="w-5 h-5 text-purple-600" />
                  <div>
                    <p className="text-sm text-gray-600">Roles</p>
                    <p className="text-2xl font-bold text-gray-900">{currentProject.selectedRoles.length}</p>
                  </div>
                </div>
              </CardContent>
            </Card>
            
            <Card>
              <CardContent className="p-4">
                <div>
                  <p className="text-sm text-gray-600 mb-2">Progress</p>
                  <Progress value={progressPercentage} className="mb-2" />
                  <p className="text-sm text-gray-500">{Math.round(progressPercentage)}% complete</p>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Kanban Board */}
          <KanbanBoard searchTerm={searchTerm} roleColors={roleColors} />
        </div>

        {/* Side Panel */}
        <div className="w-80 bg-white border-l p-6 space-y-6">
          <Card>
            <CardHeader>
              <CardTitle className="text-sm font-medium">Project Details</CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              <div>
                <p className="text-xs text-gray-500 uppercase tracking-wide">Created</p>
                <p className="text-sm text-gray-900">{currentProject.generatedAt.toLocaleDateString()}</p>
              </div>
              <div>
                <p className="text-xs text-gray-500 uppercase tracking-wide">Description</p>
                <p className="text-sm text-gray-900 line-clamp-3">{currentProject.description}</p>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="text-sm font-medium">Role Summary</CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              {currentProject.selectedRoles.map((role) => (
                <div key={role} className="flex items-center justify-between">
                  <div className="flex items-center space-x-2">
                    <div className={`w-3 h-3 rounded-full ${roleColors[role] || 'bg-gray-500'}`}></div>
                    <span className="text-sm text-gray-900">{role}</span>
                  </div>
                  <Badge variant="secondary" className="text-xs">
                    {roleTaskCounts[role]} tasks
                  </Badge>
                </div>
              ))}
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="text-sm font-medium">Quick Stats</CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              <div className="flex justify-between">
                <span className="text-sm text-gray-600">In Progress</span>
                <span className="text-sm font-medium">{columns.inProgress.length}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-sm text-gray-600">Code Review</span>
                <span className="text-sm font-medium">{columns.codeReview.length}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-sm text-gray-600">Completion Rate</span>
                <span className="text-sm font-medium">{Math.round(progressPercentage)}%</span>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
};

export default Board;
