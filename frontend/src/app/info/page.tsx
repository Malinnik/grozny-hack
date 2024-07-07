'use client';
import Sidebar from "@/components/Sidebar";
import ImageCard from "@/components/ImageCard";
import Pagination from  "@/components/Pagination";
import { use, useEffect, useState } from "react";

export interface id {
  id: string;
}

export interface page {
  page: number;
}

export default function Home() {
    const [page, setPage] = useState<number>(1);
    const [ids, setIds] = useState<id[]>([]);
    const [maxPage, setMaxPage] = useState<number>(1);


    const update = () => {
      fetch(`api/v1/images?page=${page}`, {
        method: "GET",
        })
        .then((response) => {
          if (response.ok) {
            return response.json();
          }
        })
        .then((data) => {
          setIds(data);
          console.log(ids);
      })
      fetch('api/v1/images/pages', {
        method: "GET",
        })
        .then((response) => {
          if (response.ok) {
            return response.json();
          }
        })
        .then((data) => {
          setMaxPage(data);
          console.log(maxPage);
      })
    }

    const prev_page = () => {
      if (page != 1) 
        setPage(page - 1);

    }
    const next_page = () => {
      if (page !=  maxPage)
        setPage(page  +  1);
    }
      

    useEffect(() => {
      update();
    }, [page]);

    useEffect(() => {
      update();
    }, []);

    return (
      <Sidebar active={'third'}>
        <div className="bg-gray-100">
          <div className="bg-white border max-h-[70hv] rounded-lg m-8 p-8 grid md:grid-cols-2 lg:grid-cols-3 grid-cols-1 gap-4 h-[80%]">
              {
                ids.map((id) => (
                  <ImageCard key={id.id} id={id.id}/>
                ))
              }
          </div>
          <div className="p-4 grid md:grid-cols-3 lg:grid-cols-5 grid-cols-1 gap-4">
            <Pagination page={page} max_page={maxPage} prev_page={prev_page} next_page={next_page}/>
          </div>
        </div>
      </Sidebar>
  );
}
