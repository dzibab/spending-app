import ReactDOM from 'react-dom';
import { useRef } from 'react';

import { IModalWindowProps } from 'commonTypes';

import {
  CloseButtonS,
  HeadingS,
  ModalBodyS,
  ModalWrapperS,
} from './ModalWindow.styled';
import { useClickOutside } from 'hooks';

export const ModalWindow: React.FC<IModalWindowProps> = ({
  isOpen,
  onClose,
  title,
  children,
  footer,
}) => {
  const ref = useRef<HTMLDivElement | null>(null);

  useClickOutside({ ref, callback: onClose });

  if (!isOpen) return null;

  return ReactDOM.createPortal(
    <ModalWrapperS>
      <ModalBodyS ref={ref}>
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
