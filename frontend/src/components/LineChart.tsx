"use client";

import dynamic from 'next/dynamic';
import 'chart.js/auto';
import { useEffect, useState } from 'react';
import { ChartData } from 'chart.js/auto';

const Line = dynamic(() => import('react-chartjs-2').then((mod) => mod.Line), {
  ssr: false,
});

const data: ChartData<"line", unknown, unknown> = {
  labels: ['January', 'February', 'March', 'April', 'May'],
  datasets: [
    {
      label: 'Line 1',
      data: [65, 59, 80, 81, 56],
      fill: false,
      borderColor: 'rgb(75, 192, 192)',
      tension: 0.1,
    },
    {
        label: 'Line 2',
        data: [10, 76, 36, 27, 18],
        fill: false,
        borderColor: 'rgb(255, 0, 0)',
        tension: 0.1,
      },
  ],
};



export default function LineChart() {
    const [chartData, setChartData] = useState(data);
    const [chartOptions, setChartOptions] = useState({});
    
    
    useEffect(() => {
        setChartData({
          labels: ['January', 'February', 'March', 'April', 'May'],
          datasets: [
            {
              label: 'Line 1',
              data: [65, 59, 80, 81, 56],
              fill: false,
              borderColor: 'rgb(59, 130, 246)',
              tension: 0.1,
            },
            {
              label: 'Line 2',
              data: [10, 76, 36, 27, 18],
              fill: false,
              borderColor: 'rgb(255, 0, 0)',
              tension: 0.1,
            },
          ]
        })
        setChartOptions({
          plugins: {
            legend: {
              position: 'top',
            },
            title: {
              display: 'true',
              text: 'Test Line Chart'
            }
          },
          maintainAspectRatio: false,
          responsive: true,
        })
    }, []);

    return (
      <div className='bg-white w-full md:col-span-2 relative lg:h-[70hv] h-[50vh] m-auto p-4 border rounded-lg' >
        <Line data={chartData} options={chartOptions}/>
      </div>
    );
  }