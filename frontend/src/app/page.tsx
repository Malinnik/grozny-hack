"use client";

import Sidebar from "@/components/Sidebar";
import RecentChecks from "@/components/RecentChecks";
import LineChart from "@/components/LineChart";
import { useEffect, useState } from "react";
import SubmissionTable from "@/components/SubmissionsTable";

export interface Submission  {
  id: number;
  bucket: string;
  path: string;
  created_at: string;
  status: string;
}


export default function Plot() {

  const [submissions, setSubmissions] = useState<Submission[]>([]);

  useEffect(() => {
    const result = fetch("/api/v1/submissions", {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      }
    })
    result.then((response) => {
      console.log(response)
      if (response.ok) {
        return response.json();
      }

    })
    .then((data) => {
      setSubmissions(data);
    })
    
  },[]);

  return (
    <Sidebar active={"first"}>
      <div className="bg-gray-100 h-screen">
        <div className="p-4 grid md:grid-cols-3 grid-cols-1 gap-4 h-screen overflow-y-scroll">
            {/* <LineChart />
            <RecentChecks/>
            <RecentChecks/>
            <LineChart /> */}
            <SubmissionTable data={submissions}/>
        </div>
      </div>
    </Sidebar>
  );
}
