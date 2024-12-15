export type ButtonType = 'submit' | 'button' | 'reset';
export type InputType = 'text' | 'password' | 'email';

export interface IModalWindowProps {
  isOpen: boolean;
  children: React.ReactNode;
  title?: string;
  footer?: React.ReactNode;
  onClose: VoidFunction;
}
