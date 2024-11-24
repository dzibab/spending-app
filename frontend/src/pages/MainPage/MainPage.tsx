import dayjs, { Dayjs } from 'dayjs';
import { useState } from 'react';

import { HeadingS, WrapperS } from './MainPage.styles';
import { VictoryLabel, VictoryPie, VictoryTheme } from 'victory';
import { Button } from 'components';

export const MainPage = () => {
  const today = dayjs();
  const [currentMonth, setCurrentMonth] = useState<Dayjs>(today);

  const handleChangeMonth = (isPrevious: boolean) => {
    if (isPrevious) {
      setCurrentMonth(prev => prev.subtract(1, 'month'));
    } else {
      setCurrentMonth(prev => prev.add(1, 'month'));
    }
  };

  return (
    <WrapperS>
      <HeadingS>
        <Button onClick={() => handleChangeMonth(true)}>Prev</Button>
        <h1>{currentMonth.format('MMMM')}</h1>
        <Button
          isDisabled={today.isSame(currentMonth, 'month')}
          onClick={() => handleChangeMonth(false)}
        >
          Next
        </Button>
      </HeadingS>
      {/* <input type="date" /> */}
      <div>
        <svg viewBox="0 0 200 200">
          <VictoryPie
            standalone={false}
            width={200}
            height={200}
            data={[
              { x: 'Cats', y: 30 },
              { x: 'Dogs', y: 35 },
              { x: 'Birds', y: 25 },
              { x: 'Rabbits', y: 10 },
            ]}
            innerRadius={68}
            labelRadius={50}
            theme={VictoryTheme.clean}
          />
          <VictoryLabel
            textAnchor="middle"
            style={{ fontSize: 20 }}
            x={100}
            y={100}
            text="Pets"
          />
        </svg>
      </div>
      <div>buttons</div>
    </WrapperS>
  );
};
