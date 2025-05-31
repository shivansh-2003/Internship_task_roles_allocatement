
import React from 'react';
import { useDraggable } from '@dnd-kit/core';
import { CSS } from '@dnd-kit/utilities';
import { Badge } from '@/components/ui/badge';
import { Card, CardContent } from '@/components/ui/card';
import { Task } from '@/contexts/TaskContext';
import { GripVertical, Edit, Trash2 } from 'lucide-react';
import { Button } from '@/components/ui/button';

interface TaskCardProps {
  task: Task;
  roleColor: string;
  isDragging?: boolean;
}

export const TaskCard: React.FC<TaskCardProps> = ({ task, roleColor, isDragging }) => {
  const {
    attributes,
    listeners,
    setNodeRef,
    transform,
  } = useDraggable({
    id: task.id,
  });

  const style = {
    transform: CSS.Translate.toString(transform),
  };

  return (
    <Card
      ref={setNodeRef}
      style={style}
      className={`group cursor-pointer hover:shadow-md transition-all duration-200 ${
        isDragging ? 'opacity-50 rotate-2 shadow-lg' : ''
      }`}
    >
      <CardContent className="p-4">
        {/* Drag Handle */}
        <div className="flex items-start justify-between mb-3">
          <Badge className={`text-white text-xs ${roleColor}`}>
            {task.role}
          </Badge>
          <div className="flex items-center space-x-1 opacity-0 group-hover:opacity-100 transition-opacity">
            <Button variant="ghost" size="sm" className="h-6 w-6 p-0">
              <Edit className="w-3 h-3" />
            </Button>
            <Button variant="ghost" size="sm" className="h-6 w-6 p-0 text-red-500 hover:text-red-700">
              <Trash2 className="w-3 h-3" />
            </Button>
            <div
              {...attributes}
              {...listeners}
              className="cursor-grab active:cursor-grabbing p-1 rounded hover:bg-gray-100"
            >
              <GripVertical className="w-3 h-3 text-gray-400" />
            </div>
          </div>
        </div>

        {/* Task Content */}
        <div className="space-y-2">
          <h4 className="font-medium text-gray-900 text-sm leading-tight">
            {task.title}
          </h4>
          <p className="text-xs text-gray-600 line-clamp-2">
            {task.description}
          </p>
        </div>

        {/* Task Metadata */}
        <div className="mt-3 pt-3 border-t border-gray-100">
          <div className="flex items-center justify-between text-xs text-gray-500">
            <span>Created {task.createdAt.toLocaleDateString()}</span>
            {task.updatedAt.getTime() !== task.createdAt.getTime() && (
              <span>Updated {task.updatedAt.toLocaleDateString()}</span>
            )}
          </div>
        </div>
      </CardContent>
    </Card>
  );
};
