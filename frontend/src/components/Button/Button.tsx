import { ButtonType } from 'commonTypes';
import { ButtonS } from './Button.styles';

interface IButtonProps {
  type?: ButtonType;
  className?: string;
  onClick: VoidFunction;
  children: React.ReactNode;
  isDisabled?: boolean;
  bgColor?: string
}

export const Button: React.FC<IButtonProps> = ({
  children,
  type = 'button',
  className,
  isDisabled = false,
  onClick,
  bgColor
}) => (
  <ButtonS
    disabled={isDisabled}
    type={type}
    className={className}
    onClick={onClick}
    bgColor={bgColor}
  >
    {children}
  </ButtonS>
);
