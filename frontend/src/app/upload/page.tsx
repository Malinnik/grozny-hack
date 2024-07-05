'use client';
import Sidebar from "@/components/Sidebar";
import Extrabar from "@/components/Extrabar";
import FileSelect from "@/components/FileSelect";
import { ChangeEvent, useState } from "react";

export interface Classes {
  adj: number;
  int: number;
  geo: number;
  pro: number;
  non: number;
}

export default function Home() {

  const [selectedImage, setSelectedImage] = useState<Blob>(new Blob());

  const [isImageSelected, setIsImageSelected] = useState<boolean>(false);
  const [isArchiveSelected, setIsArchiveSelected] = useState<boolean>(false);

  const [useLabel, setUseLabel] = useState<boolean>(false);
  const [showConf, setShowConf]  = useState<boolean>(false);
  
  const [sended, setSended] = useState<boolean>(false);
  
  const [showSidebar, setShowSidebar] = useState<boolean>(false);

  const imageChange = (e: ChangeEvent<HTMLInputElement>) => {

    if (e.target.files && e.target.files.length > 0) {
      const file = e.target.files[0];
      console.log(file.type);

      const valid = ["zip","application/octet-stream","application/zip","application/x-zip","application/x-zip-compressed"]

      if (valid.includes(file.type)) {
        setSelectedImage(file);
        setIsImageSelected(false);
        setIsArchiveSelected(true);
        console.log("archive selected")
      } else {
        setSelectedImage(file);
        setIsImageSelected(true);
        setIsArchiveSelected(false);
        console.log("image selected")
      }
    }
  };

  const removeSelectedImage = () => {
    setSelectedImage(new Blob());
    setIsImageSelected(false);
    setIsArchiveSelected(false);

    const element = document.getElementById('get_image_input');

    element?.focus();
    element?.classList.remove("clear-input--touched");
  };

  const handleUseLabelChange = (e: ChangeEvent<HTMLInputElement>) => {
    setUseLabel(e.target.checked);
  };

  const handleShowConfChange = (e: ChangeEvent<HTMLInputElement>) => {
    setShowConf(e.target.checked);
  };



  const handleSubmit = () => {

    if (!isImageSelected && !isArchiveSelected)
      return

    setSended(true);

    if (isImageSelected) {
      handleImageSubmit();
      return
    }
    if (isArchiveSelected) {
      handleArchiveSubmit();
      return
    }

    console.error("Cant decide what selected archive or image")

  };

  const handleImageSubmit = () => {
    let formData = new FormData();

    formData.append('file', selectedImage);
    formData.append('use_label', useLabel.toString());
    formData.append('shof_conf', showConf.toString());

    const result = fetch('/api/v1/test/upload', {
        method: 'POST',
        body: formData,
      });

    result.then((response) => {
      return response.blob();
    })
    .then((blob) => {
      setSelectedImage(blob);
      // setIsImageSelected(true);
      setSended(false);
    });
  }

  const handleArchiveSubmit = () => {
    let formData = new FormData();

    formData.append('file', selectedImage);

    const result = fetch('/api/v1/test/upload', {
        method: 'POST',
        body: formData,
      });

    result.then((response) => {
      return response.blob();
    })
    .then((blob) => {
      setSelectedImage(blob);
      setSended(false);
    });
  }


  const toggleSidebar = () => {
    setShowSidebar(!showSidebar);
  };

  return (
    <Sidebar active={'second'}>
      <div className="grid place-items-center h-screen ">
        
        <div className="w-80 sm:w-96 rounded overflow-hidden shadow-lg">
          
          <FileSelect isSended={sended} isImageSelected={isImageSelected} handleImageChange={imageChange} selectedImage={selectedImage}/>

          <div className="mt-4 flex justify-around">
            { !sended && <button onClick={removeSelectedImage} className="inline-block bg-transparent hover:bg-blue-500 text-blue-700 font-semibold hover:text-white py-2 px-4 border border-blue-500 hover:border-transparent rounded">Сбросить</button>}
            { !sended && <button onClick={handleSubmit} className="inline-block bg-transparent hover:bg-blue-500 text-blue-700 font-semibold hover:text-white py-2 px-4 border border-blue-500 hover:border-transparent rounded">Проверить</button>}
            { sended && <button disabled onClick={removeSelectedImage} className="inline-block bg-slate-400  text-white font-semibold  py-2 px-4 border rounded">Сбросить</button>}
            { sended && <button disabled onClick={handleSubmit} className="inline-block bg-slate-400  text-white font-semibold  py-2 px-4 border rounded">Ожидайте</button>}
          </div>
          
          <div className="ml-2 mt-4"> 
            <input onChange={handleUseLabelChange} type="checkbox" name="test" id="" /> <label htmlFor="">Отображать название ошибок</label>
            <br />
            <input onChange={handleShowConfChange} type="checkbox" name="test" id="" /> <label htmlFor="">Отображать процент уверенности</label>
          </div>
          
          
          <button onClick={toggleSidebar} className="fixed top-4 right-4 inline-block bg-transparent hover:bg-blue-500 text-blue-700 font-semibold hover:text-white py-2 px-4 border border-blue-500 hover:border-transparent rounded">Меню</button>
          <Extrabar toggleSidebar={toggleSidebar} showSidebar={showSidebar}/>

        </div>
      </div>
    </Sidebar>
  );
}
