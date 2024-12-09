#include "/Users/francescomarchisotti/Documents/Uni/Magistrale/Algoritmi/Libs/include/ode_solver.hpp"

#include <cmath>
#include <fstream>
#include <iomanip>
#include <iostream>

using std::cerr;
using std::cin;
using std::cout;
using std::endl;

void rangeArray(double arr[], const double &min, const double &max,
                const int &n = 1000);

void RHS(const double &t, double Y[], double R[]);

int main() {
	// Create parameter grid
	const int nPoints = 30;
	const int nStep   = 10000;

	const double minA = 0.0;
	const double maxA = 1.0;
	double gridA[nPoints + 1];
	rangeArray(gridA, minA, maxA, nPoints);

	const double minSigma = 1.0e-5;
	const double maxSigma = 1.0e-1;
	double gridSigma[nPoints + 1];
	rangeArray(gridSigma, minSigma, maxSigma, nPoints);

	std::ofstream stability, trajectory;
	stability.open("data/stability.csv");
	trajectory.open("data/trajectory.csv");
	if (!stability || !trajectory) {
		cerr << "Error: unable to open file" << endl;
		return 1;
	}

	// Init model parameters
	const double theta0 = 1.0e-7;
	const double omega0 = 0.0;  // omega0 is the initial angular velocity, not
	                            // the frequency of oscillation of the fulcrum
	const double mu = 1.0;
	const int nEq   = 5;

	const double tmin = 0.0;
	const double dt =
		1.0e-2;  // with the current parameters, the fulcrum oscillates with
	             // omega around 32, so a step size of 1.0e-2 is enough to
	             // capture the dynamics (the period of oscillation is
	             // 2π/omega = 0.2s)

	stability << "a,sigma,endpoint" << endl;
	trajectory << "t,theta,a,sigma" << endl;
	for (int iA = 0; iA <= nPoints; iA++) {
		for (int iSigma = 0; iSigma <= nPoints; iSigma++) {
			const double a     = gridA[iA];
			const double sigma = gridSigma[iSigma];

			double Y[nEq] = {theta0, omega0, sigma, a, mu};
			double t      = tmin;

			trajectory << std::setprecision(16) << t << "," << Y[0] << "," << a
					   << "," << sigma << endl;
			for (int iStep = 0; iStep < nStep; iStep++) {
				// Integration step
				rk4Step(t, Y, RHS, dt, nEq);
				t += dt;

				// This is probably not necessary
				if (fabs(Y[0]) >= M_PI) Y[0] = fmod(Y[0], 2 * M_PI);

				trajectory << std::setprecision(16) << t << "," << Y[0] << ","
						   << a << "," << sigma << endl;
			}

			stability << std::setprecision(16) << a << "," << sigma << ","
					  << Y[0] << endl;
		}
	}

	stability.close();
	trajectory.close();

	return 0;
}

void rangeArray(double arr[], const double &min, const double &max,
                const int &n) {
	const double delta = (max - min) / n;
	for (int i = 0; i <= n; i++) arr[i] = min + i * delta;
}

void RHS(const double &t, double Y[], double R[]) {
	const double theta = Y[0];
	const double omega = Y[1];
	const double sigma = Y[2];
	const double a     = Y[3];
	const double mu    = Y[4];

	R[0] = omega;
	R[1] = (sigma + a * cos(t)) * sin(theta) - mu * omega;
	R[2] = 0.0;
	R[3] = 0.0;
	R[4] = 0.0;
}
