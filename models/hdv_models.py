from dataclasses import dataclass


@dataclass
class UbicacionGeograficaData:
    departamento: str
    municipio: str
    entidad: str
    correo: str
    direccion: str
    telefono: str


@dataclass
class InformacionGeneralData:
    equipo: str
    marca: str
    modelo: str
    serie: str
    activoFijo: str
    registroSanitario: str
    ubicacion: str
    proveedor: str


@dataclass
class RegistroHistorico:
    equipo: str
    formaAdquisicion: str
    marca: str
    documento: str
    modelo: str
    añoFabricacion: str
    fechaCompra: str
    fechaInstalacion: str
    inicioOperacion: str
    vencimientoGarantia: str
    registroSanitario: str
    ubicacion: str
    proveedor: str
    fabricante: str


@dataclass
class RegistroTecnicoInstalacion:
    tension: str
    corriente: str
    peso: str
    potencia: str
    frecuencia: str
    velocidad: str
    presion: str
    rangoTemperatura: str
    tecnologiaPredominante: str


@dataclass
class RegistroTecnicoFuncionamiento:
    rangoVoltaje: str
    rangoPresion: str
    rangoHumedad: str
    rangoCorriente: str
    rangoFrecuencia: str
    diagnostico: str
    rehabilitacion: str
    prevencion: str
    tratamientoVida: str
    analisisLaboratorio: str


@dataclass
class ClasificacionBiomedica:
    rangoVoltaje: str
    diagnostico: str
    rehabilitacion: str
    prevencion: str
    tratamientoVida: str
    analisisLaboratorio: str


@dataclass
class ClasificacionNivelRiesgo:
    claseI: bool
    claseIA: bool
    claseIIB: bool
    claseIII: bool


@dataclass
class PeriodicidadMantenimiento:
    cadaTresMeses: bool
    anual: bool


@dataclass
class RequiereCalibracion:
    si: bool
    no: bool


@dataclass
class Accesorios:
    accesorio1: str
    accesorio2: str
    accesorio3: str
    accesorio4: str
    accesorio5: str
    accesorio6: str


@dataclass
class Observaciones:
    observacion1: str
    observacion2: str
    observacion3: str
    observacion4: str
    observacion5: str


# Type alias for DocumentOption
DocumentOption = str


@dataclass
class DocumentosSoportes:
    copiaRegistroSanitario: DocumentOption
    copiaRegistroImportacion: DocumentOption
    copiaFactura: DocumentOption
    copiaIngresoAlmacen: DocumentOption
    copiaActaReciboSatisfaccion: DocumentOption
    guiaRapidaOperacion: DocumentOption
    recomendacionUsoAccesorios: DocumentOption
    recomendacionAseguramientoMetrologico: DocumentOption
    estimativoCostoAccesorios: DocumentOption
    recomendacionesLimpiezaDesinfeccion: DocumentOption
    registroCapacitacion: DocumentOption
