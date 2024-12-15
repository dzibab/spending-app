import styled from 'styled-components';

export const InputWrapperS = styled.div`
  display: flex;
  flex-direction: column;
  gap: 1em;
`;

export const InputS = styled.input`
  width: 100%;
  font-size: 2em;
  border: none;
  outline: none;
  border-bottom: 1px solid gray;
  background-color: aliceblue;
  color: black;
  &[type='number']::-webkit-inner-spin-button,
  &[type='number']::-webkit-outer-spin-button {
    -webkit-appearance: none;
    margin: 0;
  }
  &[type='number'] {
    -moz-appearance: textfield;
  }
`;
