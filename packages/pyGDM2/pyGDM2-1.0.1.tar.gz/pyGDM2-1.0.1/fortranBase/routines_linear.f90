!
!    Copyright (C) 2017, P. R. Wiecha, A. Arbouet, C. Girard
!
!    This program is free software: you can redistribute it and/or modify
!    it under the terms of the GNU General Public License as published by
!    the Free Software Foundation, either version 3 of the License, or
!    (at your option) any later version.
!
!    This program is distributed in the hope that it will be useful,
!    but WITHOUT ANY WARRANTY; without even the implied warranty of
!    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
!    GNU General Public License for more details.
!
!    You should have received a copy of the GNU General Public License
!    along with this program.  If not, see <http://www.gnu.org/licenses/>.
!    
!
!
!################################################################################
!################################################################################
!
!   -------- SUBROUTINE: EXTINCT -------- 
!            Calculate Extinction/Absorption Cross-Sections
!
!################################################################################
!################################################################################

!**********************************************************************
!*
!* original code from C. Girard / A.Arbouet CEMES Toulouse
!*
!* edited as python module by P. Wiecha, CEMES, 2015-2016
!*
!**********************************************************************

      SUBROUTINE EXTINCT(ELAMBDA, &
                        & CAP, &
                        & CN2, &
                        & CEX,CEY, CEZ,&
                        & CEX0,CEY0,CEZ0, &
                        & NLAMB, NTHREADS, &
                        & NMAX, &
                        & AEXT, AABS)
      
      !f2py threadsafe
      !$ use OMP_LIB
      use OMP_LIB
      USE PYGDMPRECISION, ONLY : dp
      implicit none
      
!**********************************************************************
!*      CONFIGURATION
!**********************************************************************
      ! Fixed allocations
      real(dp), parameter :: Pi=3.141592654_dp
      complex(dp), parameter :: C0=(0._dp,0._dp)
      complex(dp), parameter :: CUN=(1._dp,0._dp)
      complex(dp), parameter :: CIM=(0._dp,1._dp)
      
      !***************************************
      !*      Structure properties  
      !***************************************
      !!! ATTENTION: Structure must be shifted to    Z(min) >= 0.5*step !!!
      integer, intent(in) :: NMAX
      complex(dp), intent(in) :: CN2    ! RefIndex: STRUCTURE SOURROUNDING(2)
      complex(dp), intent(in) :: CAP(NMAX,NLAMB) ! complex polarizabilities of meshpoints for each wavelength
      complex(dp), intent(in) :: CEX(NMAX,NLAMB), CEY(NMAX,NLAMB), CEZ(NMAX,NLAMB) ! self-consistent field inside structure
      
      ! Incident E-field (zero order)
      complex(dp), intent(in) :: CEX0(NMAX,NLAMB),CEY0(NMAX,NLAMB),CEZ0(NMAX,NLAMB)
      
      !***************************************
      !*      Simulation
      !***************************************
      integer, intent(in) :: NTHREADS
      
      ! Number and range of wavelengths (nm)
      integer, intent(in) :: NLAMB
      real(dp), intent(in)  :: ELAMBDA(NLAMB)
      
      
!**********************************************************************
!*      DECLARATION
!**********************************************************************
      integer :: NTHREADSUSE
      real(dp) :: ALAMBDA,AK0
      
      complex(dp) :: CCEX0,CCEY0,CCEZ0
      
      integer :: I, ILAMB

      complex(dp) :: CCEX(NMAX,NLAMB), CCEY(NMAX,NLAMB), CCEZ(NMAX,NLAMB)
      complex(dp) :: CPPX(NMAX,NLAMB), CPPY(NMAX,NLAMB), CPPZ(NMAX,NLAMB)
      
      complex(dp) :: CEXT(NLAMB), CABSPT(NLAMB)
      real(dp), intent(out) :: AEXT(NLAMB), AABS(NLAMB)
      
      
      complex(dp) :: CAXX(NMAX),CAYY(NMAX),CAZY(NMAX)
      complex(dp) :: CAZZ(NMAX),CAXY(NMAX),CAXZ(NMAX)
      complex(dp) :: CAYX(NMAX),CAYZ(NMAX),CAZX(NMAX)
      

!**********************************************************************
!*      INIT OPENMP
!**********************************************************************
      IF (NTHREADS==-1) THEN
        NTHREADSUSE = OMP_GET_MAX_THREADS()
      ELSE
        NTHREADSUSE = NTHREADS
      ENDIF
      CALL omp_set_num_threads(NTHREADSUSE)


!**********************************************************************
!*      Calculate Extinction Cross-Section
!**********************************************************************
!$OMP PARALLEL DEFAULT(FIRSTPRIVATE) SHARED(ELAMBDA), &
!$OMP& SHARED(CEX,CEY,CEZ, CCEX,CCEY,CCEZ), &
!$OMP& SHARED(CEX0,CEY0,CEZ0), &
!$OMP& SHARED(CPPX,CPPY,CPPZ, AEXT,AABS, CEXT,CABSPT, CAP)
!$OMP DO
        
      !P! ------- Iterate over all wavelengths - MAIN LOOP -------
      DO ILAMB=1,NLAMB
        ALAMBDA = ELAMBDA(ILAMB)
        
        !P! Wavenumber
        AK0 = 2._dp*Pi/ALAMBDA
        !! Init Arrays
        DO I=1,NMAX
            ! Complex Conjugate Efield
            CCEX(I,ILAMB) = CONJG(CEX(I,ILAMB))
            CCEY(I,ILAMB) = CONJG(CEY(I,ILAMB))
            CCEZ(I,ILAMB) = CONJG(CEZ(I,ILAMB))
        ENDDO
        
        ! Init Cross sections
        CEXT(ILAMB)=C0
        CABSPT(ILAMB)=C0
        AEXT(ILAMB)=0_dp
        AABS(ILAMB)=0_dp

        
!-----(1) Definition of the anisotropic polarizability of each -------
!---------------------discretized  cell ------------------------------
      DO I=1,NMAX
        CAXX(I)=CAP(I,ILAMB)
        CAYY(I)=CAP(I,ILAMB)
        CAZZ(I)=CAP(I,ILAMB)
        CAXY(I)=C0
        CAYX(I)=C0
        CAXZ(I)=C0
        CAZX(I)=C0
        CAZY(I)=C0
        CAYZ(I)=C0
      ENDDO
      

!------- (2) Building the vector Alpha.Eself -------------------------
!------------- (polarization at each meshpoint) ----------------------
      DO I=1,NMAX
        CPPX(I,ILAMB)=CAXX(I)*CEX(I,ILAMB) + CAXY(I)*CEY(I,ILAMB) + CAXZ(I)*CEZ(I,ILAMB)
        CPPY(I,ILAMB)=CAYX(I)*CEX(I,ILAMB) + CAYY(I)*CEY(I,ILAMB) + CAYZ(I)*CEZ(I,ILAMB)
        CPPZ(I,ILAMB)=CAZX(I)*CEX(I,ILAMB) + CAZY(I)*CEY(I,ILAMB) + CAZZ(I)*CEZ(I,ILAMB)
      ENDDO
        
        
        DO I=1,NMAX
            ! complex conjuguate of incident field
            CCEX0 = CONJG(CEX0(I,ILAMB))
            CCEY0 = CONJG(CEY0(I,ILAMB))
            CCEZ0 = CONJG(CEZ0(I,ILAMB))
            
            CEXT(ILAMB)=CEXT(ILAMB) &
                    & + (8._dp/ALAMBDA)*cn2*Pi**2*(CCEX0*CPPX(I,ILAMB) &
                    & + CCEY0*CPPY(I,ILAMB) + CCEZ0*CPPZ(I,ILAMB))
                    
            CABSPT(ILAMB)= CABSPT(ILAMB) &
                    & + (8._dp/ALAMBDA)*cn2*Pi**2 * AIMAG(CAP(I,ILAMB))* &
                    &  (   CEX(I,ILAMB)*CCEX(I,ILAMB) &
                    &    + CEY(I,ILAMB)*CCEY(I,ILAMB) &
                    &    + CEZ(I,ILAMB)*CCEZ(I,ILAMB))
        ENDDO
        AEXT(ILAMB) = AIMAG(CEXT(ILAMB)) 
        AABS(ILAMB) = REAL(CABSPT(ILAMB))      
      !P! -------------END MAIN LOOP - wavelengths ---------------
      ENDDO
      
!$OMP END DO      
!$OMP END PARALLEL 
      
      END SUBROUTINE EXTINCT








      
      
      
      
      
      
!################################################################################
!################################################################################
!
!   -------- SUBROUTINE: NEARFIELD -------- 
!            Nearfield outside structure at specific coordinates
!
!################################################################################
!################################################################################

!**********************************************************************
!*
!* original code from C. Girard CEMES Toulouse
!*
!* - edited for arbitrary coordinates, P. Wiecha, CEMES, 2015
!* - adapted for f2py, P. Wiecha, CEMES, 2015
!* - added routine for inner-particle fields, P. Wiecha, CEMES, 2015
!* - adapted for arbitrary/mixed materials, P. Wiecha, CEMES, 2016
!* - adapted as module for pyGDM2, P. Wiecha, CEMES, 2016
!*
!**********************************************************************

      SUBROUTINE NEARFIELD(ALAMBDA, SPACE, &
                    & STEP, &
                    & XM,YM,ZM, &
                    & CAP, &
                    & CN1,CN2,CN3, &
                    & CSOLX,CSOLY,CSOLZ, &
                    & CSOLBX,CSOLBY,CSOLBZ, &
                    & CEX,CEY,CEZ, &
                    & XMAP,YMAP,ZMAP, &
                    & NTHREADS, NMAX, NPTSIN, &
                    & CEPX,CEPY,CEPZ,CEPX1,CEPY1,CEPZ1, &
                    & CBPX,CBPY,CBPZ,CBPX1,CBPY1,CBPZ1)
      
      !f2py threadsafe
      !$ use OMP_LIB
      use OMP_LIB
      USE PYGDMPRECISION, ONLY : dp
      implicit none


!**********************************************************************
!*      CONFIGURATION
!**********************************************************************
      ! Fixed allocations
      real(dp), parameter :: Pi=3.141592654_dp
      complex(dp), parameter :: C0=(0._dp,0._dp)
      complex(dp), parameter :: CUN=(1._dp,0._dp)
      complex(dp), parameter :: CIM=(0._dp,1._dp)
      
      !***************************************
      !*      Structure  
      !***************************************
      !!! ATTENTION: Structure must be shifted to    Z(min) >= 0.5*step !!!
      real(dp), intent(in) :: STEP
      integer, intent(in) :: NMAX
      real(dp), intent(in) :: XM(NMAX), YM(NMAX), ZM(NMAX)
      complex(dp), intent(in) :: CAP(NMAX) ! polarizabilities
      real(dp), intent(in) :: SPACE  ! distance between substrate and top medium (nm)
      complex(dp), intent(in) :: CN1,CN2,CN3   ! RefIndex: substrate(1), environment around structure(2), top medium(3)
      
      ! self-consistent E-field inside structure
      complex(dp), intent(in) :: CEX(NMAX),CEY(NMAX),CEZ(NMAX)
      
      !***************************************
      !*      Simulation
      !***************************************
      integer, intent(in) :: NTHREADS
      
      ! wavelength
      real(dp), intent(in) :: ALAMBDA

      ! Incident field (zero order)
      complex(dp), intent(in) :: CSOLX(NPTSIN),CSOLY(NPTSIN),CSOLZ(NPTSIN)
      complex(dp), intent(in) :: CSOLBX(NPTSIN),CSOLBY(NPTSIN),CSOLBZ(NPTSIN)

      !***************************************
      !*      NF-positions definition
      !***************************************
      integer, intent(in) :: NPTSIN
      real(dp), intent(in)    :: XMAP(NPTSIN),YMAP(NPTSIN),ZMAP(NPTSIN)

      !***************************************
      !*      NF output
      !***************************************
      complex(dp), intent(out) :: CEPX(NPTSIN),CEPY(NPTSIN),CEPZ(NPTSIN)
      complex(dp), intent(out) :: CEPX1(NPTSIN),CEPY1(NPTSIN),CEPZ1(NPTSIN)
      
      complex(dp), intent(out) :: CBPX(NPTSIN),CBPY(NPTSIN),CBPZ(NPTSIN)
      complex(dp), intent(out) :: CBPX1(NPTSIN),CBPY1(NPTSIN),CBPZ1(NPTSIN)


!* ----------- DECLARATIONS
      integer :: NTHREADSUSE
      integer :: I,J,K
      integer :: ISCAN1,INI
      integer :: INSIDE

      complex(dp) :: CAXX(NMAX),CAYY(NMAX),CAZZ(NMAX)
      complex(dp) :: CAXY(NMAX),CAXZ(NMAX),CAYX(NMAX)
      complex(dp) :: CAYZ(NMAX),CAZX(NMAX),CAZY(NMAX)
      complex(dp) :: CFX(NMAX),CFY(NMAX),CFZ(NMAX)
      
      
      real(dp) :: SBB,SHORTER
      real(dp) :: AK0
      real(dp) :: XOBS,YOBS,ZOBS
      real(dp) :: XD,YD,ZD,XDDD,YDDD,ZDDD
      complex(dp) :: CEBXX,CEBXY,CEBXZ,CEBYY,CEBYZ,CEBZZ,CEBYX,CEBZX,CEBZY
      complex(dp) :: CTXX,CTXY,CTXZ,CTYY,CTYZ,CTZZ,CTYX,CTZX,CTZY
      real(dp) :: TXX1,TXY1,TXZ1,TYY1,TYZ1,TZZ1,TYX1,TZX1,TZY1
      real(dp) :: TXX2,TXY2,TXZ2,TYY2,TYZ2,TZZ2,TYX2,TZX2,TZY2
      real(dp) :: EBXY1,EBXZ1,EBYZ1,EBXY2,EBXZ2,EBYZ2

      

!**********************************************************************
!*      INIT
!**********************************************************************
      IF (NTHREADS==-1) THEN
        NTHREADSUSE = OMP_GET_MAX_THREADS()
      ELSE
        NTHREADSUSE = NTHREADS
      ENDIF
      CALL omp_set_num_threads(NTHREADSUSE)
      
      
!* Wavenumber
      AK0=2._dp*Pi/ALAMBDA
      
      
        CTXX=C0
        CTYY=C0
        CTZZ=C0
        CTXY=C0
        CTXZ=C0
        CTYZ=C0
        CTYX=C0
        CTZX=C0
        CTZY=C0
        CEBXX=C0
        CEBYY=C0
        CEBZZ=C0
        CEBXY=C0
        CEBYX=C0
        CEBXZ=C0
        CEBZX=C0
        CEBYZ=C0
        CEBZY=C0


!------------GENERATION OF THE FIELD OUTSIDE THE STRUCTURE------------
!
!-----(1) Definition of the anisotropic polarizability of each -------
!---------------------discretized  cell ------------------------------
      DO I=1,NMAX
        CAXX(I)=CAP(I)
        CAYY(I)=CAP(I)
        CAZZ(I)=CAP(I)
        CAXY(I)=C0
        CAYX(I)=C0
        CAXZ(I)=C0
        CAZX(I)=C0
        CAZY(I)=C0
        CAYZ(I)=C0
      ENDDO
      

!------- (2) Building the vector Alpha.Eself -------------------------
!------------- (polarization at each meshpoint) ----------------------
      DO K=1,NMAX
        CFX(K)=CAXX(K)*CEX(K) + CAXY(K)*CEY(K) + CAXZ(K)*CEZ(K)
        CFY(K)=CAYX(K)*CEX(K) + CAYY(K)*CEY(K) + CAYZ(K)*CEZ(K)
        CFZ(K)=CAZX(K)*CEX(K) + CAZY(K)*CEY(K) + CAZZ(K)*CEZ(K)
      ENDDO


!----------------Initialization of the vectors S*Alpha*Eself ---------
!--------------------------and E0+S*Alpha*Eself--------------------------
    DO INI=1,NPTSIN
    
    !-----Will contain S*Alpha*Eself--------------------------------------
    !-----This contribution is sometimes called the ----------------
    !-----scattered field -----------------------------------------------------
        CEPX(INI) = C0
        CEPY(INI) = C0
        CEPZ(INI) = C0
        CBPX(INI) = C0
        CBPY(INI) = C0
        CBPZ(INI) = C0
        
    !-----Will contain E0+S*Alpha*Eself-----------------------------------
    !-----This vector represents the actual field existing -----------
    !-----near around the structure ----------------------------------------
        CEPX1(INI) = C0
        CEPY1(INI) = C0
        CEPZ1(INI) = C0
        CBPX1(INI) = C0
        CBPY1(INI) = C0
        CBPZ1(INI) = C0
    ENDDO 
     

!**********************************************************************
!*      Calculate Nearfield at each defined Position
!**********************************************************************
!$OMP PARALLEL DEFAULT(FIRSTPRIVATE) SHARED(ALAMBDA,AK0), &
!$OMP& SHARED(XM,YM,ZM, XMAP,YMAP,ZMAP), &
!$OMP& SHARED(CEPX,CEPY,CEPZ,CBPX,CBPY,CBPZ), &
!$OMP& SHARED(CEPX1,CEPY1,CEPZ1,CBPX1,CBPY1,CBPZ1)
!$OMP DO

    DO ISCAN1=1,NPTSIN
      XOBS=XMAP(ISCAN1)
      YOBS=YMAP(ISCAN1)
      ZOBS=ZMAP(ISCAN1)
      SBB=STEP*1.05
      INSIDE = 0
!-----Summation on all the dicretization cells------------------------
      DO J=1,NMAX
        XD=XM(J)
        YD=YM(J)
        ZD=ZM(J)
        XDDD=XOBS-XD
        YDDD=YOBS-YD
        ZDDD=ZOBS-ZD
        SHORTER=SQRT(XDDD**2+YDDD**2+ZDDD**2) 
        IF (SHORTER.LE.SBB) THEN
            SBB=SHORTER
            INSIDE = J
            CTXX=C0
            CTYY=C0
            CTZZ=C0
            CTXY=C0
            CTXZ=C0
            CTYZ=C0
            CTYX=C0
            CTZX=C0
            CTZY=C0
            CEBXX=C0
            CEBYY=C0
            CEBZZ=C0
            CEBXY=C0
            CEBYX=C0
            CEBXZ=C0
            CEBZX=C0
            CEBYZ=C0
            CEBZY=C0
        ELSEIF ((SHORTER.GT.SBB).and.(INSIDE == 0)) then
            CALL ELECMAG0(AK0,XDDD,YDDD,ZDDD,EBXY1,EBXZ1,EBYZ1,&
	        & EBXY2,EBXZ2,EBYZ2, CN1,CN2,CN3)
            CALL PROPAGATOR123(ALAMBDA,XD,YD,ZD,&
	            & XOBS,YOBS,ZOBS,SPACE,&
	            & TXX1,TYY1,TZZ1,&
	            & TXY1,TXZ1,TYZ1,TYX1,TZX1,TZY1,&
	            & TXX2,TYY2,TZZ2,TXY2,TXZ2,TYZ2,TYX2,TZX2,TZY2,&
	            & CN1,CN2,CN3)
	    
            CTXX=TXX1*CUN+TXX2*CIM
            CTYY=TYY1*CUN+TYY2*CIM
            CTZZ=TZZ1*CUN+TZZ2*CIM
            CTXY=TXY1*CUN+TXY2*CIM
            CTXZ=TXZ1*CUN+TXZ2*CIM
            CTYZ=TYZ1*CUN+TYZ2*CIM
            CTYX=TYX1*CUN+TYX2*CIM
            CTZX=TZX1*CUN+TZX2*CIM
            CTZY=TZY1*CUN+TZY2*CIM
        !-----------------------------------------------------------------------
            CEBXX=C0
            CEBYY=C0
            CEBZZ=C0
            CEBXY=EBXY1*CUN+EBXY2*CIM
            CEBYX=-CEBXY
            CEBXZ=EBXZ1*CUN+EBXZ2*CIM
            CEBZX=-CEBXZ
            CEBYZ=EBYZ1*CUN+EBYZ2*CIM
            CEBZY=-CEBYZ
        ENDIF
        if (INSIDE == 0) then
        !------ Outside structure, propagate field -------------
        !------ Cell-volume (for integration) is taken into 
        !------ account in the polarizability CF_I
            CEPX(ISCAN1)=CEPX(ISCAN1)&
                            & + CTXX*CFX(J)+CTXY*CFY(J)&
                            & + CTXZ*CFZ(J)
            CEPY(ISCAN1)=CEPY(ISCAN1)&
                            & + CTYX*CFX(J)+CTYY*CFY(J)&
                            & + CTYZ*CFZ(J)
            CEPZ(ISCAN1)=CEPZ(ISCAN1)&
                            & + CTZX*CFX(J)+CTZY*CFY(J)&
                            & + CTZZ*CFZ(J)
        !----------------------------------------------------------------------
            CBPX(ISCAN1)=CBPX(ISCAN1)&
                            & + CEBXX*CFX(J)+CEBXY*CFY(J)&
                            & + CEBXZ*CFZ(J)
            CBPY(ISCAN1)=CBPY(ISCAN1)&
                            & + CEBYX*CFX(J)+CEBYY*CFY(J)&
                            & + CEBYZ*CFZ(J)
            CBPZ(ISCAN1)=CBPZ(ISCAN1)&
                            & + CEBZX*CFX(J)+CEBZY*CFY(J)&
                            & + CEBZZ*CFZ(J)
         endif
      ENDDO
      if (INSIDE /= 0) then
!       write(*,*), " --> in", CEX(INSIDE),CEY(INSIDE)
      !------ Inside structure, take E-field at closest meshpoint, having index "INSIDE" -------------
        CEPX(ISCAN1)=CEX(INSIDE)
        CEPY(ISCAN1)=CEY(INSIDE)
        CEPZ(ISCAN1)=CEZ(INSIDE)
      !-------- the magnetic field inside the structure cannot be obtained 
      !-------- using the propagator for the self-consistent field and must 
      !-------- be calculated differently (e.g. using the corresponding 
      !-------- Greens function for the self-consistent scattering problem, or 
      !-------- by explicitly calculating the curl using numerical differentiation)
        CBPX(ISCAN1)=C0
        CBPY(ISCAN1)=C0
        CBPZ(ISCAN1)=C0
      endif

      
      !* ---------------------------------------------------
      !* ---- E-field with fundamental field ----
      !* ---------------------------------------------------  
      CEPX1(ISCAN1) = CEPX(ISCAN1) + CSOLX(ISCAN1)
      CEPY1(ISCAN1) = CEPY(ISCAN1) + CSOLY(ISCAN1)
      CEPZ1(ISCAN1) = CEPZ(ISCAN1) + CSOLZ(ISCAN1)

      !* ---------------------------------------------------
      !* ---- B-field with fundamental field ----
      !* ---------------------------------------------------  
      CBPX1(ISCAN1) = CBPX(ISCAN1) + CSOLBX(ISCAN1)
      CBPY1(ISCAN1) = CBPY(ISCAN1) + CSOLBY(ISCAN1)
      CBPZ1(ISCAN1) = CBPZ(ISCAN1) + CSOLBZ(ISCAN1)
     
     
      !* End loop over NF-positions
      ENDDO

!$OMP END DO      
!$OMP END PARALLEL 

      END SUBROUTINE NEARFIELD






    
    
    
    
    
    
    
    
    
    
!**********************************************************************
!*      Calculate Far-field radiation from dipoles above substrate
!**********************************************************************

!**************************************************************
!   SUBROUTINE DIPOLE RADIATION FAR-FIELD
!         C. GIRARD, A. ARBOUET - CEMES - 2013
!         originally from: G. Colas des Francs, C. Girard
!   UNITS = nanometers
!
!   Adapted for f2py as python module 2017 by P. Wiecha
!
!**************************************************************
!
!**************** Implemented following **********************
! Francs, G. C. des, Girard, C. & Dereux, A.
! Theory of near-field optical imaging with a single molecule 
! as light source. 
! The Journal of Chemical Physics 117, 4659–4666 (2002).
!**************************************************************  
!**************************************************************

subroutine DIPOLEFARFIELD(r,teta,phi, &
                                & xd,yd,zd, &
                                & cpx, cpy, cpz,&
                                & eps0,eps1,alambda, &
                                & cex, cey, cez)
      
      
      USE PYGDMPRECISION, ONLY : dp
      implicit none
      
      complex(dp), parameter :: C0=(0._dp,0._dp)
      complex(dp), parameter :: CUN=(1._dp,0._dp)
      complex(dp), parameter :: CIM=(0._dp,1._dp)
      real(dp), parameter    :: Pi=3.141592654_dp

      real(dp), intent(in)  :: r,teta,phi           ! Position at which to compute E-field (spherical coordinates)
      real(dp), intent(in)  :: xd,yd,zd            ! Position of radiating dipole
      complex(dp), intent(in)  :: cpx, cpy, cpz     ! complex dipole moment components
      complex(dp), intent(in)  :: eps0, eps1        ! dielectric constant of substrate and environment
                                                    ! (eps0 respectively eps1)
      real(dp), intent(in)  :: alambda            ! radiation wavelength (nm)
      
      complex(dp), intent(out) :: cex,cey,cez   ! COMPUTED E-field at (X,Y,Z)
      
      complex(dp) :: SsurfXX,SsurfXY,SsurfXZ,SsurfYX,SsurfYY,SsurfYZ,SsurfZX,SsurfZY,SsurfZZ
      complex(dp) :: SvacXX,SvacXY,SvacXZ,SvacYX,SvacYY,SvacYZ,SvacZX,SvacZY,SvacZZ
      complex(dp) :: SXX,SXY,SXZ,SYX,SYY,SYZ,SZX,SZY,SZZ
      complex(dp) :: Asurf, Avac ! common terms of propagators
      complex(dp) :: rs,rp
      complex(dp) :: ak0, ak_substrate, eps_diff
      


!**************************************************************
!***************** COMPUTATION PARAMETERS *********************
!**************************************************************
       ak_substrate = 2.*Pi*sqrt(eps0)/alambda     ! wavevector in substrate
       ak0 = 2.*Pi*sqrt(eps1)/alambda              ! wavevector in particle environment
       eps_diff = (eps0 - eps1 + 1._dp)            ! relative permittivity
       
!        X = r*sin(teta)*cos(phi)
!        Y = r*sin(teta)*sin(phi)
!        Z = r*cos(teta)
       
!!!!! ABOVE SUBSTRATE ( Z=r*cos(teta) )
if (r*cos(teta) > 0) then
!**************************************************************
!******************* Surface propagator ***********************
!**************************************************************
      rs = (cos(teta)-sqrt(eps_diff-(sin(teta))**2))/(cos(teta)+sqrt(eps_diff-(sin(teta))**2))
      rp = (eps_diff*cos(teta)-sqrt(eps_diff-(sin(teta))**2))/(eps_diff*cos(teta)+sqrt(eps_diff-(sin(teta))**2))

      
      Asurf = -ak0**2*exp(cim*ak0*r) / r * &
                       & exp(-cim*ak0*SIN(teta)*(COS(phi)*xd+SIN(phi)*yd)) * &
                       & exp(cim*ak0*COS(teta)*zd)

          SsurfXX =  rp*(COS(teta))**2*(COS(phi))**2 - rs*(SIN(phi))**2 
          SsurfXY =  (rp*(COS(teta))**2+rs)*SIN(phi)*COS(phi)
          SsurfXZ =  rp*SIN(teta)*COS(teta)*COS(phi)
          SsurfYX =  SsurfXY
          SsurfYY =  rp*(COS(teta))**2*(SIN(phi))**2 - rs*(COS(phi))**2  ! modif !
          SsurfYZ =  rp*SIN(teta)*COS(teta)*SIN(phi)
          SsurfZX =  -rp*SIN(teta)*COS(teta)*COS(phi)  
          SsurfZY =  -rp*SIN(teta)*COS(teta)*SIN(phi)        
          SsurfZZ =  -rp*(SIN(teta))**2


          SsurfXX =  Asurf*SsurfXX
          SsurfXY =  Asurf*SsurfXY
          SsurfXZ =  Asurf*SsurfXZ
          SsurfYX =  Asurf*SsurfYX
          SsurfYY =  Asurf*SsurfYY
          SsurfYZ =  Asurf*SsurfYZ
          SsurfZX =  Asurf*SsurfZX
          SsurfZY =  Asurf*SsurfZY
          SsurfZZ =  Asurf*SsurfZZ

!**************************************************************
!******************* Vacuum propagator ************************
!**************************************************************

      Avac = ak0**2*exp(cim*ak0*r) / r * &
           & exp(-cim*ak0*SIN(teta)*(COS(phi)*xd+SIN(phi)*yd)) * &
           & exp(-cim*ak0*COS(teta)*zd)

          SvacXX =  1._dp-(SIN(teta))**2*(COS(phi))**2
          SvacXY =  -(SIN(teta))**2*COS(phi)*SIN(phi)
          SvacXZ =  -SIN(teta)*COS(teta)*COS(phi)
          SvacYX =  -(SIN(teta))**2*COS(phi)*SIN(phi)
          SvacYY =  1._dp-(SIN(teta))**2*(SIN(phi))**2
          SvacYZ =  -SIN(teta)*COS(teta)*SIN(phi)
          SvacZX =  -SIN(teta)*COS(teta)*COS(phi)
          SvacZY =  -SIN(teta)*COS(teta)*SIN(phi)
          SvacZZ =  (SIN(teta))**2
      
          SvacXX =  Avac*SvacXX
          SvacXY =  Avac*SvacXY
          SvacXZ =  Avac*SvacXZ
          SvacYX =  Avac*SvacYX
          SvacYY =  Avac*SvacYY
          SvacYZ =  Avac*SvacYZ
          SvacZX =  Avac*SvacZX
          SvacZY =  Avac*SvacZY
          SvacZZ =  Avac*SvacZZ 

!**************************************************************
!******************* Total propagator *************************
!**************************************************************

          SXX =  SvacXX + SsurfXX
          SXY =  SvacXY + SsurfXY
          SXZ =  SvacXZ + SsurfXZ
          SYX =  SvacYX + SsurfYX
          SYY =  SvacYY + SsurfYY
          SYZ =  SvacYZ + SsurfYZ
          SZX =  SvacZX + SsurfZX
          SZY =  SvacZY + SsurfZY
          SZZ =  SvacZZ + SsurfZZ  

!!!!! BELOW SUBSTRATE ( Z=r*cos(teta) )
elseif (r*cos(teta) <= 0) then
        
!**************************************************************
!******* TESTING:  Vacuum propagator ***********************
!**************************************************************
        Avac = ak0**2*exp(cim*ak0*r) / r * &
                         & exp(-cim*ak0*SIN(teta)*(COS(phi)*xd+SIN(phi)*yd)) * &
                         & exp(-cim*ak0*COS(teta)*zd)

          SvacXX =  1._dp-(SIN(teta))**2*(COS(phi))**2
          SvacXY =  -(SIN(teta))**2*COS(phi)*SIN(phi)
          SvacXZ =  -SIN(teta)*COS(teta)*COS(phi)
          SvacYX =  -(SIN(teta))**2*COS(phi)*SIN(phi)
          SvacYY =  1._dp-(SIN(teta))**2*(SIN(phi))**2
          SvacYZ =  -SIN(teta)*COS(teta)*SIN(phi)
          SvacZX =  -SIN(teta)*COS(teta)*COS(phi)
          SvacZY =  -SIN(teta)*COS(teta)*SIN(phi)
          SvacZZ =  (SIN(teta))**2
      
          SXX =  Avac*SvacXX
          SXY =  Avac*SvacXY
          SXZ =  Avac*SvacXZ
          SYX =  Avac*SvacYX
          SYY =  Avac*SvacYY
          SYZ =  Avac*SvacYZ
          SZX =  Avac*SvacZX
          SZY =  Avac*SvacZY
          SZZ =  Avac*SvacZZ 
        

        
else

        SXX = -999999
        SXY = -999999
        SXZ = -999999
        SYX = -999999
        SYY = -999999
        SYZ = -999999
        SZX = -999999
        SZY = -999999
        SZZ = -999999


endif        
!**************************************************************
!******************* COMPUTING E-FIELD ************************
!**************************************************************
          
          cex = SXX*cpx + SXY*cpy + SXZ*cpz
          cey = SYX*cpx + SYY*cpy + SYZ*cpz
          cez = SZX*cpx + SZY*cpy + SZZ*cpz
          
          end subroutine DIPOLEFARFIELD

          

    
    

!******************************************************************
! far-field polarization from NPOL dipoles ABOVE surface (eps1)
!******************************************************************

!**************************************************************
!   SUBROUTINE MULTI DIPOLE RADIATION TO FAR-FIELD
!               polarization filtered in image-plane
!
!         P. WIECHA, A. ARBOUET - CEMES - 2014
!
!   Adapted for f2py python module 2017 by P. Wiecha
!
!**************************************************************

      subroutine MULTIDIPOLEFARFIELD(ALAMBDA, Ntetasca, Nphi, &
                     & tetamin, tetamax, &
                     & r, eps0, eps1, polarizerangle, &
                     & XDP,YDP,ZDP, &
                     & CPPX,CPPY,CPPZ, &
                     & NDP, NTHREADS, &
                     & tetalist, philist, &
                     & IntensInt, IntensIntPol, IntensPol, Intens, &
                     & cexSC, ceySC, cezSC, ceSCpol)
      
!                      & CEX0,CEY0,CEZ0, &
      
      !f2py threadsafe
      !$ use OMP_LIB
      use OMP_LIB
      USE PYGDMPRECISION, ONLY : dp
      implicit none
      
      !! Constants
      complex(dp), parameter :: c0=(0._dp,0._dp)
      complex(dp), parameter :: cun=(1._dp,0._dp)
      complex(dp), parameter :: cim=(0._dp,1._dp)
      real(dp), parameter :: Pi=3.141592654_dp
      
      
      !! Input
      integer, intent(in)           :: NDP
      integer, intent(in)           :: Ntetasca,Nphi
      real(dp), intent(in)  :: tetamin, tetamax
      real(dp), intent(in)  :: polarizerangle
      real(dp), intent(in)  :: r, ALAMBDA
      complex(dp), intent(in)    :: eps0, eps1
      real(dp), DIMENSION(NDP), intent(in) :: XDP,YDP,ZDP                ! dipoles positions
      complex(dp), DIMENSION(NDP), intent(in) :: CPPX,CPPY,CPPZ    ! electric polarization of structure dipoles
      integer, intent(in) :: NTHREADS
!       complex(dp), DIMENSION(Ntetasca, Nphi), intent(in) :: CEX0,CEY0,CEZ0    ! precalculated fundamental field at sphere
      
      
      !! Output
      real(dp), intent(out)         :: IntensInt, IntensIntPol
      real(dp), DIMENSION(Ntetasca, Nphi), intent(out) :: tetalist, philist
      complex(dp), DIMENSION(Ntetasca, Nphi), intent(out) :: cexSC, ceySC, cezSC, ceSCpol
      real(dp), DIMENSION(Ntetasca, Nphi), intent(out)       :: Intens
      real(dp), DIMENSION(Ntetasca, Nphi), intent(out) :: IntensPol
      
      
      !! Internally used
      real(dp) :: dteta, dphi, dSurf, tetasca, phi
      integer          :: Itetasca, Iphi, IS

      complex(dp) :: CEX, CEY, CEZ
      complex(dp) :: cexSCtmp, ceySCtmp, cezSCtmp
      complex(dp)   :: CEPPAR, CEPPERP, CEPPOL
      
      integer :: NTHREADSUSE
      
      
      !! OpenMP Parallel
      IF (NTHREADS==-1) THEN
        NTHREADSUSE = OMP_GET_MAX_THREADS()
      ELSE
        NTHREADSUSE = NTHREADS
      ENDIF
      CALL omp_set_num_threads(NTHREADSUSE)
      
      
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!         Calculate Farfield and extract polarization
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
      dteta = (tetamax-tetamin)/(Ntetasca-1._dp)  ! teta: tetamin --> tetamax, including 'tetamax'
      dphi = 2._dp*Pi/(Nphi)                     ! phi: 0 - 360deg --> excluding 360deg

!$OMP PARALLEL DO DEFAULT(SHARED) &
!$OMP& FIRSTPRIVATE(r,tetasca,phi, dphi,dteta, &
!$OMP&              eps0,eps1,ALAMBDA, cexSCtmp,ceySCtmp,cezSCtmp, &
!$OMP&              CEX, CEY, CEZ, polarizerangle, CEPPAR,CEPPERP,CEPPOL)
      ! Numerical Integration
       DO Itetasca=1,Ntetasca
         DO Iphi=1,Nphi
           
           tetasca = tetamin + (Itetasca-1._dp)*dteta
           phi = (Iphi-1._dp)*dphi
           
           tetalist(Itetasca,Iphi) = tetasca
           philist(Itetasca,Iphi) = phi
           
           cexSCtmp = C0
           ceySCtmp = C0
           cezSCtmp = C0
            
           DO IS=1,NDP
!**************************************************************
!            COMPUTING E-FIELD intensity in far-field
!**************************************************************
             call DIPOLEFARFIELD(r,tetasca,phi, &
                        & XDP(IS), YDP(IS), ZDP(IS), &
                        & CPPX(IS), CPPY(IS), CPPZ(IS), &
                        & eps0, eps1, ALAMBDA, &
                        & CEX, CEY, CEZ)
                   
             cexSCtmp = cexSCtmp + CEX
             ceySCtmp = ceySCtmp + CEY
             cezSCtmp = cezSCtmp + CEZ
           ENDDO ! end of Do loop on dipoles
      
           cexSC(Itetasca,Iphi) = cexSCtmp
           ceySC(Itetasca,Iphi) = ceySCtmp
           cezSC(Itetasca,Iphi) = cezSCtmp
            
!**************************************************************
!            EXTRACT INTENSITY ALONG POLARIZATIONS
!**************************************************************
           ! Components parallel/perp. to polarizer
             CEPPAR = cexSCtmp*COS(phi)*COS(tetasca) + &
                          & ceySCtmp*SIN(phi)*COS(tetasca) - &
                          & cezSCtmp*SIN(tetasca)                  ! Scattered E-field parallel to scattering plane
             CEPPERP = cexSCtmp*SIN(phi) - &
                            & ceySCtmp*COS(phi)                      ! Scattered E-field perpendicular to scattering plane
             CEPPOL = CEPPAR*COS(polarizerangle-phi) - &
                          & CEPPERP*SIN(polarizerangle-phi)   ! Scattered E-field parallel to polarizer
             ceSCpol(Itetasca,Iphi) = CEPPOL
            
             ! total and polarization-filtered intensities at teta/phi-position
             Intens(Itetasca,Iphi) = (abs(cexSCtmp)**2 + abs(ceySCtmp)**2 + abs(cezSCtmp)**2)
             IntensPol(Itetasca,Iphi) = ABS(CEPPOL)**2
           
         ENDDO ! end of Do loop on phi
       ENDDO ! end of Do loop on tetasca
!$OMP END PARALLEL DO
      

! integrate intensities in non-parallel loop
       IntensInt = 0._dp
       IntensIntPol = 0._dp
       DO Itetasca=1,Ntetasca
       tetasca =  tetamin + (Itetasca-1._dp)*dteta
       dSurf = r**2*SIN(tetasca)*dteta*dphi  ! <-- solid-angle surface element
       
         DO Iphi=1,Nphi
            IntensInt      = IntensInt + Intens(Itetasca,Iphi) * dSurf 
            IntensIntPol = IntensIntPol + IntensPol(Itetasca,Iphi) * dSurf 
         ENDDO ! end of Do loop on phi
       ENDDO ! end of Do loop on tetasca


      END SUBROUTINE MULTIDIPOLEFARFIELD
      
      
      











