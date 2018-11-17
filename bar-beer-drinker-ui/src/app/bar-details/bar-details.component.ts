import { Component, OnInit } from '@angular/core';
import {ActivatedRoute} from '@angular/router';
import {BarsService, Bar, BarMenuItem} from '../bars.service'
import { HttpResponse } from '@angular/common/http';


@Component({
  selector: 'app-bar-details',
  templateUrl: './bar-details.component.html',
  styleUrls: ['./bar-details.component.css']
})
export class BarDetailsComponent implements OnInit {
  barName: string;
  barDetails: Bar[];
  menu: BarMenuItem[];

  constructor(
    private barservice: BarsService,
    private route: ActivatedRoute
  ) { 
    route.paramMap.subscribe((paramMap)=>{
      this.barName=paramMap.get('bar');

      barservice.getBar(this.barName).subscribe(
        data=>{
          this.barDetails =data;
        },
        (error:HttpResponse<any>)=>{
          if (error.status ===404){
            alert('Bar Not Found');
          }
          else{
            console.error(error.status+'-'+error.body);
            alert('An error occured on the Server. Please check browser console');
          }
        }
      );
      barservice.getMenu(this.barName).subscribe(
        data=> {
          this.menu = data;
        },
        
      );
    });
  }

  ngOnInit() {
  }

}
