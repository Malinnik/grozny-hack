"use client";

import Sidebar from "@/components/Sidebar";
import RecentChecks from "@/components/RecentChecks";
import LineChart from "@/components/LineChart";


export default function Plot() {
  return (
    <Sidebar active={"first"}>
      <div className="bg-gray-100 h-screen">
        <div className="p-4 grid md:grid-cols-3 grid-cols-1 gap-4 h-screen overflow-y-scroll">
            <LineChart />
            <RecentChecks/>
            <RecentChecks/>
            <LineChart />
        </div>
      </div>
    </Sidebar>
  );
}
