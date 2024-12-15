import { HTMLInputTypeAttribute } from 'react';
import { InputS, InputWrapperS } from './Input.styled';

interface IInputProps {
  default?: boolean;
  error?: string;
  name?: string;
  onChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
  placeholder?: string;
  type: HTMLInputTypeAttribute;
  value: string | number;
}

export const Input: React.FC<IInputProps> = ({
  type,
  value,
  onChange,
  error,
  placeholder,
}) => (
  <InputWrapperS>
    <InputS
      type={type}
      value={value}
      onChange={onChange}
      placeholder={placeholder}
    />
    {error && <span>{error}</span>}
  </InputWrapperS>
);
