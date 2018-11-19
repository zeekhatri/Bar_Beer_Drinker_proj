import { Component, OnInit } from '@angular/core';
import {ActivatedRoute} from '@angular/router';
import {BarsService, Bar, BarMenuItem} from '../bars.service'
import { HttpResponse } from '@angular/common/http';

declare const Highcharts: any;

@Component({
  selector: 'app-bar-details',
  templateUrl: './bar-details.component.html',
  styleUrls: ['./bar-details.component.css']
})
export class BarDetailsComponent implements OnInit {
  barName: string;
  barDetails: Bar[];
  menu: BarMenuItem[];
  drinkers: any[];
  beers: any[]; 

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

      this.barservice.get_top_drinkers(this.barName).subscribe(
        data=>{
          this.drinkers=data;
        }
      );

      this.barservice.get_top_beers(this.barName).subscribe(
        data=>{
          this.beers=data;
        }
      );

      this.barservice.getBusyBarDays(this.barName).subscribe(
        data=>{
          console.log(data);

          const day=[];
        const busyday=[];

        data.forEach(bar => {
          day.push(bar.Day);
          busyday.push(bar.busyday);
        });
        
        this.renderCharts(day, busyday);
        }
      );
    });
  }

  ngOnInit() {
  }

  renderCharts(day: string[], busyday: number[]) {
    Highcharts.chart('bargraph', {
      chart: {
        type: 'column'
      },
      title: {
        text: 'Transactions on different days'
      },
      xAxis: {
        categories: day,
        title: {
          text: 'Day'
        }
      },
      yAxis: {
        min: 0,
        title: {
          text: 'No of Transactions'
        },
        labels: {
          overflow: 'justify'
        }
      },
      plotOptions: {
        bar: {
          datalabels: {
            enabled: true
          }
        }
      },
      legend: {
        enabled: false
      },
      credits: {
        enabled: false
      },
      series: [{
        data: busyday
      }]

    });
  }
}
