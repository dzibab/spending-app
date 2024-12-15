import { IModalWindowProps } from 'commonTypes';
import { Button, Input, ModalWindow } from 'components';
import { BodyS, ModalContainerS } from './AddSpending.styled';
import { useState } from 'react';

type AddSpendingModalProps = Omit<IModalWindowProps, 'children'>;

export const AddSpendingModal: React.FC<AddSpendingModalProps> = ({
  isOpen,
  onClose,
}) => {
  const [value, setValue] = useState<string | number>('');

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    setValue(value);
  };

  return (
    <ModalWindow isOpen={isOpen} onClose={onClose}>
      <ModalContainerS>
        <BodyS>
          <Input
            type="number"
            value={value}
            onChange={handleChange}
            placeholder="Write your spending"
          />
          <div>Categories</div>
        </BodyS>
        <Button bgColor="blue" onClick={() => {}}>
          Confirm
        </Button>
      </ModalContainerS>
    </ModalWindow>
  );
};
