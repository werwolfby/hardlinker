import { Injectable }      from '@angular/core';
import { Http }            from '@angular/http';
import { URLSearchParams } from '@angular/http';
import { Observable }      from "rxjs";
import { FileInfo }        from "./browse.service";
import "rxjs/add/operator/map";

@Injectable()
export class GuessItService {
    constructor (private _http: Http) {        
    }

    guessit(fileInfo: FileInfo) : Observable<FileInfo> {
        let params : URLSearchParams = new URLSearchParams();
        params.set('folder', fileInfo.folder);
        params.set('path', [...fileInfo.path, fileInfo.name].join('/'));

        return this._http
            .get(`api/guess/it`, { search: params })
            .map(r => <FileInfo> r.json());
    }
}
