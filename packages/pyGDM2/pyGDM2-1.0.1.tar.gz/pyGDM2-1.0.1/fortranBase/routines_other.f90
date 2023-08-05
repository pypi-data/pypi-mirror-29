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
!!*********************************************************************
! Author: Peter Wiecha
! CEMES/CNRS 
!
! Date: Dec. 2017
!
!*********************************************************************

      SUBROUTINE RELOCATE_CLOSE_POINTS( &
                    & step, mindist, projection, &
                    & NPT, XMap,YMap,ZMap, &
                    & NMAX, XObj,YObj,ZObj, &
                    & Xout, Yout, Zout, &
                    & nthreads)
      
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
      real(dp), intent(in) :: projection ! 0: none, 1: XZ, 2: XY, 3: YZ
      real(dp), intent(in) :: step, mindist
      
      integer, intent(in) :: NMAX, NPT
      real(dp), intent(in) :: XMap(NPT), YMap(NPT), ZMap(NPT)
      real(dp), intent(in) :: XObj(NMAX), YObj(NMAX), ZObj(NMAX)
      
      
      !***************************************
      !*      openmp
      !***************************************
      integer, intent(in) :: NTHREADS
      
      
      !***************************************
      !*      output
      !***************************************
      real(dp), intent(out) :: Xout(NPT), Yout(NPT), Zout(NPT)
      
      
      !***************************************
      !*      OTHER DECLARATIONS
      !***************************************
      integer :: NTHREADSUSE
      
      !* ----------- Temporary Propagators
      real(dp) :: XObs,YObs,ZObs,  Xi,Yi,Zi,  Xj,Yj,Zj
      real(dp) :: XD,YD,ZD, XDDD,YDDD,ZDDD, SBB, SHORTER
      
      integer :: I,J, IMAP, INSIDE
      
      
      
      
      
!**********************************************************************
!*      Configure
!**********************************************************************
      IF (NTHREADS==-1) THEN
        NTHREADSUSE = OMP_GET_MAX_THREADS()
      ELSE
        NTHREADSUSE = NTHREADS
      ENDIF
      CALL omp_set_num_threads(NTHREADSUSE)
      
      
!* --- Double loop points 
!$OMP PARALLEL DEFAULT(FIRSTPRIVATE) SHARED(NMAX, NPT), &
!$OMP& SHARED(XMAP,YMAP,ZMAP,XObj,YObj,ZObj,Xout,Yout,Zout)
!$OMP DO
      DO IMAP=1,NPT
        XObs = XMap(IMAP)
        YObs = YMap(IMAP)
        ZObs = ZMap(IMAP)
        
        
        !* --- Check if inside or outside of structure
        SBB=STEP*mindist
        INSIDE = 0
        DO J=1,NMAX
            XD = XObj(J)
            YD = YObj(J)
            ZD = ZObj(J)
            XDDD = XObs-XD
            YDDD = YObs-YD
            ZDDD = ZObs-ZD
            
            if ((projection == 0).OR.(&
              & (projection==1).AND.(YD==YObs)).OR.(&
              & (projection==2).AND.(ZD==ZObs)).OR.(&
              & (projection==3).AND.(XD==XObs))) THEN
                SHORTER=SQRT(XDDD**2+YDDD**2+ZDDD**2) 
            ELSE
                SHORTER=5*SBB
            ENDIF
            
            IF (SHORTER.LE.SBB) THEN
              !* --- inside structure: get index of closest meshpoint
              SBB=SHORTER
              INSIDE = J
            ENDIF
        ENDDO        
        
!!!*** =======================================
!!!*** INSIDE STRUCTURE
!!!*** =======================================
        IF (INSIDE /= 0) THEN
        Xout(IMAP) = XObj(INSIDE)
        Yout(IMAP) = YObj(INSIDE)
        Zout(IMAP) = ZObj(INSIDE)

!!!*** =======================================
!!!*** OUTSIDE STRUCTURE
!!!*** =======================================
        ELSEIF (INSIDE == 0) THEN
        Xout(IMAP) = XMap(IMAP)
        Yout(IMAP) = YMap(IMAP)
        Zout(IMAP) = ZMap(IMAP)
        ENDIF
       
      ENDDO
!$OMP END DO
!$OMP END PARALLEL 

      END



