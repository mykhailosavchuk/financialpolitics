import { ComponentFixture, TestBed, waitForAsync } from '@angular/core/testing';

import { NewsEditorComponent } from './news-editor.component';

describe('NewsEditorComponent', () => {
  let component: NewsEditorComponent;
  let fixture: ComponentFixture<NewsEditorComponent>;

  beforeEach(waitForAsync(() => {
    TestBed.configureTestingModule({
      declarations: [ NewsEditorComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(NewsEditorComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
