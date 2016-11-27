import { Injectable } from '@angular/core';
import { Http }       from '@angular/http';
import { Observable } from "rxjs";
import { FileInfo } from "./browse.service";
import "rxjs/add/operator/map";

@Injectable()
export class GuessItService {
    constructor (private _http: Http) {        
    }

    guessit(fileInfo: FileInfo) : Observable<FileInfo> {
        const filePath = [...fileInfo.path, fileInfo.name].join('/');

        return this._http
            .get(`api/guessit?folder=${fileInfo.folder}&filepath=${filePath}`)
            .map(r => <FileInfo> r.json());
    }
}
