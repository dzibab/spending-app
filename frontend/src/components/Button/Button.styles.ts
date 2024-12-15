import styled from 'styled-components';

export const ButtonS = styled.button.withConfig({
  shouldForwardProp: prop => prop !== 'bgColor',
})<{ bgColor?: string }>`
  border: none;
  outline: none;
  cursor: pointer;
  font-size: 2em;
  width: 100%;
  background-color: ${props => props.bgColor || 'transparent'};
`;
