import io
from typing import Union,Any
import aiohttp

# TODO: skip queue virustotal 
class VirusTotalAPI:
    def __init__(self,apikey:str,local_telegram_api:bool):
        self.apikey = apikey
        self.local_telegram_api = local_telegram_api
        
    async def __download_file(self,filepath:str,
            *args,**kw) -> Union[io.BytesIO,Any]:

        if ( self.local_telegram_api ):
            with open(filepath,'rb') as bf:
                return io.BytesIO(bf.read())
        else:
            from load import bot
            return await bot.download_file(filepath,
            *args,**kw)
    
    async def __file_scan(self,filepath) -> None:
        file = await self.__download_file(filepath)

        url = "https://www.virustotal.com/vtapi/v2/file/scan"
        params = {"apikey":self.apikey,"file":file}

        async with aiohttp.ClientSession() as session:
            response = await session.post(url,data=params)
            response = await response.json()

        return response["sha1"]
    
    async def __file_report(self,resource) -> dict:
        url = "https://www.virustotal.com/vtapi/v2/file/report"
        params = {"apikey":self.apikey,"resource":resource}
        
        async with aiohttp.ClientSession() as session:
            response = await session.get(url,params=params)
            response = await response.json()

        return response

    def format_output(self,file_report:dict) -> str:
        """Format file_report
            File Analys 
            Status:Infected/Clear
            Positives:positives/total percent%
            File Report
        """ 

        total     = file_report["total"]
        positives = file_report["positives"]
        permalink = file_report["permalink"]
        percent   = round(positives/total*100)
        
        if (percent >= 40):
            status = "Infected ☣️"
        else:
            status = "Clear ✅"
         
        output = (
            (
                "File Analys\n"
                f"Detected:{positives}/{total} %{percent}\n"
                f"Status:{status}\n"
                f"[File Report]({permalink})\n"
            )
        )

        return output
    
    async def scan_file(self,filepath:str) -> str:
        resource = await self.__file_scan(filepath)
        file_report = await self.__file_report(resource)
        
        return file_report
