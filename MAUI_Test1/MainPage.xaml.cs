using M335_FirstTimeMAUI.ViewModel;

namespace M335_FirstTimeMAUI
{
    public partial class MainPage : ContentPage
    {
    
        public MainPage(MainViewModel vm)
        {
            InitializeComponent();
            BindingContext = vm;
        }


    }

}
