Summary:	Return to Castle Wolfenstein
Summary(pl.UTF-8):   Return to Castle Wolfenstein (Powrót do zamku Wolfenstein)
Name:		rtcw
Version:	1.41
%define		_subver	3
Release:	1
Vendor:		id Software
License:	RTCW EULA, PB EULA
Group:		Applications/Games
Source0:	ftp://ftp.idsoftware.com/idstuff/wolf/linux/wolf-linux-%{version}-%{_subver}.x86.run
# Source0-md5:	1db2a23a9548c8d84c8f9dbe87963842
Source1:	http://www.evenbalance.com/downloads/pbweb.x86
NoSource:	1
Source2:	rtcw.init
Source3:	rtcw.sysconfig
URL:		http://www.idsoftware.com/
Requires(post,preun):	/sbin/chkconfig
Requires:	OpenGL
Requires:	psmisc
Requires:	screen
ExclusiveArch:	%{ix86}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		no_install_post_strip	1

%define		_noautoreqdep	libGL.so.1 libGLU.so.1
%define		_gamedir	%{_datadir}/%{name}

%description
World War II rages and nations fall. SS head Himmler has
Hitler's full backing to twist science and the occult into an
army capable of annihilating the Allies once and for all.
Battling alone, you're on an intense mission to pierce the
black heart of the Third Reich and stop Himmler -- or die
trying.

%description -l pl.UTF-8
Druga Wojna Światowa szaleje, a nacje upadają. Dowódca SS,
Heinrich Himmler, w pełni wspierany przez Adolfa Hitlera,
prowadzi tajemnicze eksperymenty łączące naukę z okultyzmem.
Ich celem jest stworzenie armii zdolnej do zadania całkowitej
klęski wojskom alianckim. Twoje zadanie to przebić czarne
serce Trzeciej Rzeszy i powstrzymać Himmlera. Albo tego
dokonasz, albo zginiesz na polu walki.

%prep
%setup -qcT
sh %{SOURCE0} --tar xf

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/{rc.d/init.d,sysconfig},%{_gamedir}/{main,pb/{,htm}},%{_bindir}}

install %{SOURCE1} $RPM_BUILD_ROOT%{_bindir}
install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/rtcw
install %{SOURCE3} $RPM_BUILD_ROOT/etc/sysconfig/rtcw
cp -rf main/* $RPM_BUILD_ROOT%{_gamedir}/main
install bin/Linux/x86/*.x86 $RPM_BUILD_ROOT%{_gamedir}
install pb/*.so $RPM_BUILD_ROOT%{_gamedir}/pb
install pb/htm/*.htm $RPM_BUILD_ROOT%{_gamedir}/pb/htm

cat << EOF > $RPM_BUILD_ROOT%{_bindir}/rtcw-sp
#!/bin/sh
cd %{_gamedir}
./wolfsp.x86
EOF
cat << EOF > $RPM_BUILD_ROOT%{_bindir}/rtcw-mp
#!/bin/sh
cd %{_gamedir}
./wolf.x86
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add rtcw

echo ""
echo "You need to copy pak*.pk3 from RTCW CD installation into %{_gamedir}/main/."
echo "Or if you have got a Windows installation of RTCW make a symlink to save space."
echo ""
echo "To start a dedicated server, run /etc/rc.d/init.d/rtcw start"
echo ""

%preun
if [ "$1" = "0" ]; then
	/sbin/chkconfig --del rtcw
fi

%files
%defattr(644,root,root,755)
%doc RTCW-README-1.4.txt Docs
%attr(755,root,root) %{_bindir}/rtcw*
%attr(754,root,root) /etc/rc.d/init.d/rtcw
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/rtcw
%dir %{_gamedir}
%{_gamedir}/main
%dir %{_gamedir}/pb
%{_gamedir}/pb/htm
%attr(755,root,root) %{_gamedir}/pb/*.so
%attr(754,root,games) %{_gamedir}/wolf*x86
%attr(755,root,root) %{_bindir}/pbweb.x86
