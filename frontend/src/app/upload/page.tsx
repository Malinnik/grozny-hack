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
  const [useLabel, setUseLabel] = useState<boolean>(false);
  const [showConf, setShowConf]  = useState<boolean>(false);
  
  const [sended, setSended] = useState<boolean>(false);
  
  const [showSidebar, setShowSidebar] = useState<boolean>(false);

  const [responseText, setResponseText] = useState<Classes>(JSON.parse('{"adj": 0, "int": 0, "geo": 0, "pro": 0, "non": 0}'));

  const imageChange = (e: ChangeEvent<HTMLInputElement>) => {

    if (e.target.files && e.target.files.length > 0) {
      setSelectedImage(e.target.files[0]);
      setIsImageSelected(true);
    }
  };

  const removeSelectedImage = () => {
    setSelectedImage(new Blob());
    setIsImageSelected(false);
    setResponseText(JSON.parse('{"adj": 0, "int": 0, "geo": 0, "pro": 0, "non": 0}'))

    const element = document.getElementById('get_image_input');
    
    element?.focus();
    element?.classList.remove("clear-input--touched")
  };

  const handleUseLabelChange = (e: ChangeEvent<HTMLInputElement>) => {
    setUseLabel(e.target.checked);
  };

  const handleShowConfChange = (e: ChangeEvent<HTMLInputElement>) => {
    setShowConf(e.target.checked);
  };


  const handleSubmit = () => {

    if (!isImageSelected)
      return

    setSended(true);

    let formData = new FormData();

    formData.append('file', selectedImage);
    formData.append('use_label', useLabel.toString());
    formData.append('shof_conf', showConf.toString());

    const result = fetch('/api/v1/test/upload', {
      method: 'POST',
      body: formData,
    });

    result.then((response) => {
      let text = response.statusText;  
      console.log(text);
      let res = text.split(' ');
      console.log(res)

      let classes: Classes = {adj: Number(res[0]), 
        int: Number(res[1]),
        geo: Number(res[2]),
        pro: Number(res[3]),
        non: Number(res[4])
      }
      
      console.log(classes)

      setResponseText(classes);
     
      return response.blob();
    })
    .then((blob) => {
      setSelectedImage(blob);
      setSended(false);
    });

  };

  const toggleSidebar = () => {
    setShowSidebar(!showSidebar);
  };

  return (
    <Sidebar active={'second'}>
      <div className="grid place-items-center h-screen ">
        
        <div className="w-80 sm:w-96 rounded overflow-hidden shadow-lg">
          
          <FileSelect isImageSelected={isImageSelected} handleImageChange={imageChange} selectedImage={selectedImage}/>

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
          <Extrabar responseText={responseText} toggleSidebar={toggleSidebar} showSidebar={showSidebar}/>

        </div>
      </div>
    </Sidebar>
  );
}
