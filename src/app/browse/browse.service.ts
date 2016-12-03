import { Injectable }                         from '@angular/core';
import { Http }                               from '@angular/http';
import { URLSearchParams }                    from '@angular/http';
import { Observable }                         from "rxjs"
import { FileInfo, LinkInfo, FileInfoObject } from "./file-info";
import "rxjs/add/operator/map";

const LINKS_API_PATH = 'api/links';

@Injectable()
export class BrowseService {
    constructor (private _http: Http) {        
    }

    getAll() : Observable<FileInfoObject[]> {
        return this._http
            .get(LINKS_API_PATH)
            .map(r => {
                const result = <LinkInfo[]> r.json();
                return result.map(l => new FileInfoObject(l));
            });
    }

    link(src : FileInfo, dest : FileInfo) : Observable<LinkInfo> {
        let params : URLSearchParams = new URLSearchParams();
        params.set('folder', src.folder);
        params.set('path', [...src.path, src.name].join('/'));
        
        return this._http
            .post(LINKS_API_PATH, JSON.stringify(dest), { search: params })
            .map(r => {
                let result = <LinkInfo> r.json();
                result.links = [dest];
                return result;
            });
    }
}
