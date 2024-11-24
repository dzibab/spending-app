import { ButtonType } from 'commonTypes';
import { ButtonS } from './Button.styles';

interface IButtonProps {
  type?: ButtonType;
  className?: string;
  onClick: VoidFunction;
  children: React.ReactNode;
  isDisabled?: boolean;
}

export const Button: React.FC<IButtonProps> = ({
  children,
  type = 'button',
  className,
  isDisabled = false,
  onClick,
}) => (
  <ButtonS
    disabled={isDisabled}
    type={type}
    className={className}
    onClick={onClick}
  >
    {children}
  </ButtonS>
);
