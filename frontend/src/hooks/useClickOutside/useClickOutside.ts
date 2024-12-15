import { useEffect } from 'react';

interface IUseClickOutsideProps {
  ref: React.RefObject<HTMLElement>;
  callback: VoidFunction;
}

export const useClickOutside = ({ ref, callback }: IUseClickOutsideProps) => {
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (ref.current && !ref.current.contains(event.target as Node)) {
        callback();
      }
    };

    document.addEventListener('mousedown', handleClickOutside);

    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [ref, callback]);
};
