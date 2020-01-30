{
    'name':'Recruitment Report',
    'version': '12.5',
    'category': 'STPI',
    'author': 'Dexciss Technology by RGupta',
    'description':""" 
      Last updated by    
     Report of Curated Report   """ ,
    'website': 'https://www.dexciss.com',
    'license': 'AGPL-3',
    
   'depends': ['base','stpi_hr_recruitment'],
   
   # Officer of hr_attendance groups has been given to all menuitems of report
   # hr_branch_company,external_layout_branch,base_branch_company for report
   
    'data': [
        'security/ir.model.access.csv',
        'wizard/late_coming_wizard_view.xml',
        'report/late_coming.xml',
        'view/late_coming_report.xml',

        
    ],
    'demo': [
       
    ],
    'installable': True,
}
