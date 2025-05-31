
import React from 'react';
import {
  DndContext,
  DragEndEvent,
  DragOverlay,
  DragStartEvent,
  PointerSensor,
  useSensor,
  useSensors,
} from '@dnd-kit/core';
import { Task, useTask } from '@/contexts/TaskContext';
import { KanbanColumn } from './KanbanColumn';
import { TaskCard } from './TaskCard';

interface KanbanBoardProps {
  searchTerm: string;
  roleColors: Record<string, string>;
}

export const KanbanBoard: React.FC<KanbanBoardProps> = ({ searchTerm, roleColors }) => {
  const { state, dispatch } = useTask();
  const [activeTask, setActiveTask] = React.useState<Task | null>(null);

  const sensors = useSensors(
    useSensor(PointerSensor, {
      activationConstraint: {
        distance: 8,
      },
    })
  );

  const columns = [
    { id: 'todo', title: 'TO DO', color: 'border-blue-200 bg-blue-50' },
    { id: 'inProgress', title: 'IN PROGRESS', color: 'border-yellow-200 bg-yellow-50' },
    { id: 'codeReview', title: 'CODE REVIEW', color: 'border-purple-200 bg-purple-50' },
    { id: 'done', title: 'DONE', color: 'border-green-200 bg-green-50' },
  ];

  const filteredTasks = (columnTasks: Task[]) => {
    if (!searchTerm) return columnTasks;
    return columnTasks.filter(task => 
      task.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
      task.description.toLowerCase().includes(searchTerm.toLowerCase()) ||
      task.role.toLowerCase().includes(searchTerm.toLowerCase())
    );
  };

  const handleDragStart = (event: DragStartEvent) => {
    const { active } = event;
    const task = Object.values(state.columns)
      .flat()
      .find(task => task.id === active.id);
    setActiveTask(task || null);
  };

  const handleDragEnd = (event: DragEndEvent) => {
    const { active, over } = event;
    setActiveTask(null);

    if (!over) return;

    const taskId = active.id as string;
    const newColumn = over.id as string;

    // Find the current column of the task
    const currentColumn = Object.entries(state.columns).find(([_, tasks]) =>
      tasks.some(task => task.id === taskId)
    )?.[0];

    if (currentColumn && currentColumn !== newColumn) {
      dispatch({
        type: 'MOVE_TASK',
        payload: {
          taskId,
          fromColumn: currentColumn,
          toColumn: newColumn,
        },
      });
    }
  };

  return (
    <DndContext sensors={sensors} onDragStart={handleDragStart} onDragEnd={handleDragEnd}>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 h-full">
        {columns.map((column) => {
          const columnTasks = state.columns[column.id as keyof typeof state.columns];
          const tasks = filteredTasks(columnTasks);
          
          return (
            <KanbanColumn
              key={column.id}
              id={column.id}
              title={column.title}
              color={column.color}
              tasks={tasks}
              roleColors={roleColors}
            />
          );
        })}
      </div>

      <DragOverlay>
        {activeTask ? (
          <TaskCard
            task={activeTask}
            roleColor={roleColors[activeTask.role] || 'bg-gray-500'}
            isDragging
          />
        ) : null}
      </DragOverlay>
    </DndContext>
  );
};
