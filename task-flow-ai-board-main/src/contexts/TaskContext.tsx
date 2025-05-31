
import React, { createContext, useContext, useReducer, ReactNode } from 'react';

export interface Task {
  id: string;
  title: string;
  description: string;
  role: string;
  status: 'todo' | 'inProgress' | 'codeReview' | 'done';
  createdAt: Date;
  updatedAt: Date;
}

export interface Project {
  description: string;
  generatedAt: Date;
  selectedRoles: string[];
  tasks: Task[];
}

interface TaskState {
  currentProject: Project | null;
  columns: {
    todo: Task[];
    inProgress: Task[];
    codeReview: Task[];
    done: Task[];
  };
  loading: boolean;
  error: string | null;
  filters: {
    searchTerm: string;
    selectedRoles: string[];
  };
}

type TaskAction =
  | { type: 'SET_LOADING'; payload: boolean }
  | { type: 'SET_ERROR'; payload: string | null }
  | { type: 'SET_PROJECT'; payload: Project }
  | { type: 'MOVE_TASK'; payload: { taskId: string; fromColumn: string; toColumn: string } }
  | { type: 'SET_FILTER'; payload: Partial<TaskState['filters']> }
  | { type: 'RESET_PROJECT' };

const initialState: TaskState = {
  currentProject: null,
  columns: {
    todo: [],
    inProgress: [],
    codeReview: [],
    done: [],
  },
  loading: false,
  error: null,
  filters: {
    searchTerm: '',
    selectedRoles: [],
  },
};

const taskReducer = (state: TaskState, action: TaskAction): TaskState => {
  switch (action.type) {
    case 'SET_LOADING':
      return { ...state, loading: action.payload };
    case 'SET_ERROR':
      return { ...state, error: action.payload };
    case 'SET_PROJECT':
      const tasks = action.payload.tasks;
      return {
        ...state,
        currentProject: action.payload,
        columns: {
          todo: tasks,
          inProgress: [],
          codeReview: [],
          done: [],
        },
      };
    case 'MOVE_TASK':
      const { taskId, fromColumn, toColumn } = action.payload;
      const fromTasks = [...state.columns[fromColumn as keyof typeof state.columns]];
      const toTasks = [...state.columns[toColumn as keyof typeof state.columns]];
      
      const taskIndex = fromTasks.findIndex(task => task.id === taskId);
      if (taskIndex === -1) return state;
      
      const [movedTask] = fromTasks.splice(taskIndex, 1);
      movedTask.status = toColumn as Task['status'];
      movedTask.updatedAt = new Date();
      toTasks.push(movedTask);
      
      return {
        ...state,
        columns: {
          ...state.columns,
          [fromColumn]: fromTasks,
          [toColumn]: toTasks,
        },
      };
    case 'SET_FILTER':
      return {
        ...state,
        filters: { ...state.filters, ...action.payload },
      };
    case 'RESET_PROJECT':
      return initialState;
    default:
      return state;
  }
};

const TaskContext = createContext<{
  state: TaskState;
  dispatch: React.Dispatch<TaskAction>;
} | null>(null);

export const TaskProvider = ({ children }: { children: ReactNode }) => {
  const [state, dispatch] = useReducer(taskReducer, initialState);
  return (
    <TaskContext.Provider value={{ state, dispatch }}>
      {children}
    </TaskContext.Provider>
  );
};

export const useTask = () => {
  const context = useContext(TaskContext);
  if (!context) {
    throw new Error('useTask must be used within a TaskProvider');
  }
  return context;
};
