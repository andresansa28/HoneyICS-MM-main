export interface Container {
    IP: string;
    name: string;
}

export interface DeployModel {
    name: string;
    IP: string;
    user: string;
    passw: string;
    active: boolean;
    Containers : Container[];
}

export interface DeploymentsModel {
    delay: number;
    MaxMind_GeoDB_Key: string;
    RemoteDeployments: DeployModel[];
}
