import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class BartendersService {

  constructor(private http: HttpClient) { }

  get_bartenders(){
    return this.http.get<any[]>('/api/bartender')
  }

}
