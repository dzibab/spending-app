import ReactDOM from 'react-dom';
import {
  CloseButtonS,
  HeadingS,
  ModalBodyS,
  ModalWrapperS,
} from './ModalWindow.styled';
import { IModalWindowProps } from 'commonTypes';

export const ModalWindow: React.FC<IModalWindowProps> = ({
  isOpen,
  onClose,
  title,
  children,
  footer,
}) => {
  if (!isOpen) return null;

  return ReactDOM.createPortal(
    <ModalWrapperS>
      <ModalBodyS>
        <HeadingS>
          {title && <p>{title}</p>}
          <CloseButtonS onClick={onClose}>X</CloseButtonS>
        </HeadingS>
        {children}
        {footer && <div>{footer}</div>}
      </ModalBodyS>
    </ModalWrapperS>,
    document.body
  );
};
