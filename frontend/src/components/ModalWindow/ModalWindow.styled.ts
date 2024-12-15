import styled from 'styled-components';

export const ModalWrapperS = styled.div`
  position: fixed;
  background-color: rgba(0, 0, 0, 0.5);
  top: 0;
  left: 0;
  bottom: 0;
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
`;

export const ModalBodyS = styled.div`
  position: absolute;
  padding: 2rem 2rem;
  background-color: aliceblue;
  border-radius: 1em;
  max-width: 80vw;
  min-width: 20vw;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
  color: black;
  overflow: hidden;
  min-height: 20vh;
`;

export const CloseButtonS = styled.button`
  background-color: transparent;
  position: absolute;
  top: 0;
  right: 0;
  color: black;
  text-align: right;
  outline: none;
  border: none;
  cursor: pointer;
`;

export const HeadingS = styled.div`
  position: relative;
  width: 100%;
`;
