
import React from 'react';
import { useDroppable } from '@dnd-kit/core';
import { Badge } from '@/components/ui/badge';
import { Task } from '@/contexts/TaskContext';
import { TaskCard } from './TaskCard';

interface KanbanColumnProps {
  id: string;
  title: string;
  color: string;
  tasks: Task[];
  roleColors: Record<string, string>;
}

export const KanbanColumn: React.FC<KanbanColumnProps> = ({
  id,
  title,
  color,
  tasks,
  roleColors,
}) => {
  const { setNodeRef } = useDroppable({ id });

  return (
    <div className={`flex flex-col h-full`}>
      {/* Column Header */}
      <div className={`${color} border rounded-t-lg p-4 flex items-center justify-between`}>
        <h3 className="font-semibold text-gray-700">{title}</h3>
        <Badge variant="secondary" className="bg-white/70">
          {tasks.length}
        </Badge>
      </div>

      {/* Column Content */}
      <div
        ref={setNodeRef}
        className="flex-1 bg-white border border-t-0 rounded-b-lg p-4 space-y-3 min-h-[500px] overflow-y-auto"
      >
        {tasks.map((task) => (
          <TaskCard
            key={task.id}
            task={task}
            roleColor={roleColors[task.role] || 'bg-gray-500'}
          />
        ))}
        
        {tasks.length === 0 && (
          <div className="flex items-center justify-center h-32 text-gray-400 text-sm">
            Drop tasks here
          </div>
        )}
      </div>
    </div>
  );
};
