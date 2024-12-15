import ReactDOM from 'react-dom';
import {
  CloseButtonS,
  HeadingS,
  ModalBodyS,
  ModalWrapperS,
} from './ModalWindow.styled';

interface IModalWindow {
  isOpen: boolean;
  children: React.ReactNode;
  title?: string;
  footer?: React.ReactNode;
  onClose: VoidFunction;
}

export const ModalWindow: React.FC<IModalWindow> = ({
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
